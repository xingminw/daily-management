#!/usr/bin/env python3
"""zju-mail — ZJU (@zju.edu.cn, Coremail) mailbox wrapper over IMAP/SMTP.

Credentials never live in this repo:
  macOS Keychain item: service "zju-mail", account = email address, password = mail password.
  Env overrides for testing: ZJU_MAIL_ADDR / ZJU_MAIL_PASS.

Server info (public, from ZJU IT Center):
  IMAP  imap.zju.edu.cn  993 (SSL)      SMTP  smtp.zju.edu.cn  994 (SSL)

Subcommands:
  test                                     login + capability check
  folders                                  list all folders
  list [-f INBOX] [-n 10] [--unread] [--since 2026-08-01]
  read <uid> [-f INBOX]                    full message body + attachment names
  search <query> [-f INBOX] [-n 20]        subject/from/body keyword search
  attachments <uid> [-f INBOX] [-d DIR]    list (or download) attachments
  send --to a@x.com,b@x.com [--cc ...] --subject S --body B [--attach FILE ...]
  reply <uid> --body B [-f INBOX] [--all]  reply with quoted original
  draft [--to ...] [--cc ...] --subject S --body B [-f FOLDER]
                                           save a draft into the server Drafts folder
  mark <uid> [--seen|--unseen] [--flag|--unflag] [--keyword KW ...] [-f INBOX]
                                           set/clear IMAP flags (labels)

Output: single JSON object per run.
  {"ok": true, "data": ...}  |  {"ok": false, "error": "..."}   (exit code 1)
"""

import argparse
import base64
import email
import imaplib
import json
import os
import re
import smtplib
import subprocess
import sys
from email import encoders
from email.header import Header, decode_header, make_header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import getaddresses, make_msgid, parseaddr

IMAP_HOST = "imap.zju.edu.cn"
IMAP_PORT = 993
SMTP_HOST = "smtp.zju.edu.cn"
SMTP_PORT = 994
KEYCHAIN_SERVICE = "zju-mail"


# ---------------------------------------------------------------- credentials

def keychain_password():
    r = subprocess.run(
        ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-w"],
        capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def keychain_account():
    r = subprocess.run(
        ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE],
        capture_output=True, text=True)
    m = re.search(r'"acct"<blob>="([^"]*)"', r.stdout)
    return m.group(1) if m else None


def get_credentials():
    addr = os.environ.get("ZJU_MAIL_ADDR") or keychain_account()
    pwd = os.environ.get("ZJU_MAIL_PASS") or keychain_password()
    if not addr or not pwd:
        fail("credentials not found: store once via "
             'security add-generic-password -s zju-mail -a "<you>@zju.edu.cn" '
             '-w "<password>", or export ZJU_MAIL_ADDR / ZJU_MAIL_PASS', code=2)
    return addr, pwd


# ---------------------------------------------------------------- output

def out(data):
    print(json.dumps({"ok": True, "data": data}, ensure_ascii=False, indent=2))


def fail(msg, code=1):
    print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
    sys.exit(code)


# ---------------------------------------------------------------- imap utf-7

def utf7_encode(name):
    res, buf = [], ""
    for ch in name:
        if 0x20 <= ord(ch) <= 0x7E:
            if buf:
                res.append(_b64mod(buf) + "-")
                buf = ""
            res.append("&-" if ch == "&" else ch)
        else:
            buf += ch
    if buf:
        res.append(_b64mod(buf) + "-")
    return "".join(res)


def _b64mod(s):
    return "&" + base64.b64encode(s.encode("utf-16-be")).decode().rstrip("=").replace("/", ",")


def utf7_decode(name):
    res, i = [], 0
    while i < len(name):
        if name[i] == "&":
            j = name.find("-", i + 1)
            if j == -1:
                res.append(name[i + 1:])
                break
            seg = name[i + 1:j]
            if seg == "":
                res.append("&")
            else:
                pad = "=" * ((4 - len(seg) % 4) % 4)
                try:
                    res.append(base64.b64decode(
                        seg.replace(",", "/") + pad).decode("utf-16-be"))
                except Exception:
                    res.append(seg)
            i = j + 1
        else:
            res.append(name[i])
            i += 1
    return "".join(res)


# ---------------------------------------------------------------- helpers

def dec_hdr(value):
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return str(value)


def imap_connect():
    addr, pwd = get_credentials()
    try:
        m = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    except Exception as e:
        fail(f"cannot reach {IMAP_HOST}:{IMAP_PORT}: {e}", code=3)
    # Some Coremail builds require an IMAP ID command before login.
    try:
        m._simple_command("ID", '("name" "zju-mail" "version" "1.0")')
    except Exception:
        pass
    try:
        m.login(addr, pwd)
    except imaplib.IMAP4.error as e:
        fail(f"login failed for {addr}: {e} (check Keychain password)", code=4)
    return m, addr


def select_folder(m, folder, readonly=True):
    typ, data = m.select(utf7_encode(folder), readonly=readonly)
    if typ != "OK":
        fail(f"cannot select folder {folder!r}: {data}")


def find_folder(m, *keywords):
    """Return the first folder whose (decoded) name contains any keyword."""
    typ, data = m.list()
    for item in data or []:
        s = item.decode() if isinstance(item, bytes) else str(item)
        mm = re.search(r'(?:"((?:[^"\\]|\\.)*)")\s*$', s)
        if not mm:
            continue
        name = mm.group(1).replace('\\"', '"')
        decoded = utf7_decode(name)
        for kw in keywords:
            if kw.lower() in name.lower() or kw.lower() in decoded:
                return decoded
    return None


def parse_fetch_pair(item):
    """imaplib fetch item -> (meta_str, raw_bytes)"""
    meta, raw = "", b""
    if isinstance(item, tuple):
        meta = item[0].decode("utf-8", "replace") if isinstance(item[0], bytes) else str(item[0])
        raw = item[1] if isinstance(item[1], bytes) else b""
    elif isinstance(item, bytes):
        meta = item.decode("utf-8", "replace")
    return meta, raw


def summary_from_raw(uid, meta, raw):
    msg = email.message_from_bytes(raw)
    flags = re.search(r"FLAGS \(([^)]*)\)", meta)
    return {
        "uid": uid,
        "from": dec_hdr(msg.get("From", "")),
        "to": dec_hdr(msg.get("To", "")),
        "subject": dec_hdr(msg.get("Subject", "")),
        "date": dec_hdr(msg.get("Date", "")),
        "unread": "\\Seen" not in (flags.group(1) if flags else ""),
    }


def body_text(msg):
    """Best-effort plain-text body (falls back to stripped HTML)."""
    plain, html = None, None
    for part in msg.walk():
        if part.is_multipart():
            continue
        ctype = part.get_content_type()
        disp = (part.get("Content-Disposition") or "")
        if "attachment" in disp:
            continue
        payload = part.get_payload(decode=True)
        if payload is None:
            continue
        charset = part.get_content_charset() or "utf-8"
        try:
            text = payload.decode(charset, "replace")
        except LookupError:
            text = payload.decode("utf-8", "replace")
        if ctype == "text/plain" and plain is None:
            plain = text
        elif ctype == "text/html" and html is None:
            html = text
    if plain is not None:
        return plain
    if html is not None:
        return re.sub(r"<[^>]+>", " ", re.sub(r"(?i)<(br|/p|/div)>", "\n", html))
    return ""


def attachment_list(msg):
    atts = []
    for part in msg.walk():
        fname = part.get_filename()
        if fname:
            atts.append({
                "filename": dec_hdr(fname),
                "content_type": part.get_content_type(),
                "size": len(part.get_payload(decode=True) or b""),
            })
    return atts


# ---------------------------------------------------------------- commands

def cmd_test(args):
    m, addr = imap_connect()
    typ, caps = m.capability()
    m.logout()
    out({"account": addr, "imap": f"{IMAP_HOST}:{IMAP_PORT}", "capabilities": caps[0].decode() if caps and caps[0] else ""})


def cmd_folders(args):
    m, _ = imap_connect()
    typ, data = m.list()
    folders = []
    for item in data or []:
        s = item.decode() if isinstance(item, bytes) else str(item)
        mm = re.search(r'(?:"((?:[^"\\]|\\.)*)")\s*$', s)
        if mm:
            folders.append(utf7_decode(mm.group(1).replace('\\"', '"')))
    m.logout()
    out({"folders": folders})


def cmd_list(args):
    m, addr = imap_connect()
    select_folder(m, args.folder)
    crit = ["UNSEEN"] if args.unread else ["ALL"]
    if args.since:
        crit += ["SINCE", args.since]
    typ, data = m.search(None, *crit)
    if typ != "OK":
        fail(f"search failed: {data}")
    uids = [u for u in data[0].split() if u][-args.limit:]
    items = []
    for u in reversed(uids):
        typ, fd = m.fetch(u, "(UID FLAGS BODY.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE)])")
        for it in fd:
            meta, raw = parse_fetch_pair(it)
            if raw:
                items.append(summary_from_raw(u.decode(), meta, raw))
    m.logout()
    out({"account": addr, "folder": args.folder, "count": len(items), "messages": items})


def cmd_read(args):
    m, addr = imap_connect()
    select_folder(m, args.folder)
    typ, fd = m.fetch(args.uid, "(BODY.PEEK[])")
    raw = None
    for it in fd:
        if isinstance(it, tuple):
            raw = it[1]
    if raw is None:
        fail(f"uid {args.uid} not found in {args.folder}")
    msg = email.message_from_bytes(raw)
    m.logout()
    out({
        "account": addr,
        "uid": args.uid,
        "folder": args.folder,
        "from": dec_hdr(msg.get("From", "")),
        "to": dec_hdr(msg.get("To", "")),
        "cc": dec_hdr(msg.get("Cc", "")),
        "subject": dec_hdr(msg.get("Subject", "")),
        "date": dec_hdr(msg.get("Date", "")),
        "body": body_text(msg),
        "attachments": attachment_list(msg),
    })


def cmd_search(args):
    m, addr = imap_connect()
    select_folder(m, args.folder)
    query = args.query
    try:
        typ, data = m.search("UTF-8", "SUBJECT", query)
        if typ != "OK" or not data[0].split():
            typ, data = m.search("UTF-8", "TEXT", query)
    except imaplib.IMAP4.error:
        typ, data = m.search(None, "SUBJECT", f'"{query}"')
    if typ != "OK":
        fail(f"search failed: {data}")
    uids = [u for u in data[0].split() if u][-args.limit:]
    items = []
    for u in reversed(uids):
        typ, fd = m.fetch(u, "(UID FLAGS BODY.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE)])")
        for it in fd:
            meta, raw = parse_fetch_pair(it)
            if raw:
                items.append(summary_from_raw(u.decode(), meta, raw))
    m.logout()
    out({"account": addr, "query": query, "count": len(items), "messages": items})


def cmd_attachments(args):
    m, addr = imap_connect()
    select_folder(m, args.folder)
    typ, fd = m.fetch(args.uid, "(BODY.PEEK[])")
    raw = None
    for it in fd:
        if isinstance(it, tuple):
            raw = it[1]
    if raw is None:
        fail(f"uid {args.uid} not found in {args.folder}")
    msg = email.message_from_bytes(raw)
    atts = attachment_list(msg)
    downloaded = []
    if args.download:
        os.makedirs(args.download, exist_ok=True)
        for part in msg.walk():
            fname = part.get_filename()
            if not fname:
                continue
            safe = os.path.basename(dec_hdr(fname).replace("\\", "/"))
            payload = part.get_payload(decode=True) or b""
            path = os.path.join(args.download, safe)
            base, ext = os.path.splitext(path)
            n = 1
            while os.path.exists(path):
                path = f"{base}({n}){ext}"
                n += 1
            with open(path, "wb") as f:
                f.write(payload)
            downloaded.append(path)
    m.logout()
    out({"account": addr, "uid": args.uid, "attachments": atts, "downloaded": downloaded})


def build_mime(addr, to_list, cc_list, subject, body, attach_paths):
    msg = MIMEMultipart()
    msg["From"] = addr
    if to_list:
        msg["To"] = ", ".join(to_list)
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)
    msg["Subject"] = Header(subject, "utf-8")
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="zju.edu.cn")
    msg.attach(MIMEText(body, "plain", "utf-8"))
    for path in attach_paths:
        if not os.path.isfile(path):
            fail(f"attachment not found: {path}")
        with open(path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment",
                        filename=os.path.basename(path))
        msg.attach(part)
    return msg


def smtp_send(addr, pwd, msg, to_list, cc_list):
    s = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    try:
        s.login(addr, pwd)
        s.send_message(msg, from_addr=addr, to_addrs=to_list + cc_list)
    finally:
        s.quit()


def cmd_send(args):
    addr, pwd = get_credentials()
    msg = build_mime(addr, args.to, args.cc, args.subject, args.body, args.attach)
    smtp_send(addr, pwd, msg, args.to, args.cc)
    out({"sent_from": addr, "to": args.to, "cc": args.cc, "subject": args.subject})


def cmd_reply(args):
    m, addr = imap_connect()
    select_folder(m, args.folder)
    typ, fd = m.fetch(args.uid, "(BODY.PEEK[])")
    raw = None
    for it in fd:
        if isinstance(it, tuple):
            raw = it[1]
    if raw is None:
        fail(f"uid {args.uid} not found in {args.folder}")
    orig = email.message_from_bytes(raw)
    m.logout()

    orig_from = dec_hdr(orig.get("From", ""))
    orig_subject = dec_hdr(orig.get("Subject", ""))
    orig_msgid = orig.get("Message-ID", "").strip()
    quoted = "\n".join("> " + line for line in body_text(orig).splitlines())
    body = args.body + "\n\n" + \
        f"在 {dec_hdr(orig.get('Date', ''))}，{orig_from} 写道：\n" + quoted

    to_list = [parseaddr(orig_from)[1]]
    cc_list = []
    if args.all:
        for _, a in getaddresses(orig.get_all("To", []) + orig.get_all("Cc", [])):
            if a and a != addr and a not in to_list:
                cc_list.append(a)

    msg = MIMEMultipart()
    msg["From"] = addr
    msg["To"] = ", ".join(to_list)
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)
    msg["Subject"] = Header(orig_subject if orig_subject.lower().startswith("re:")
                            else "Re: " + orig_subject, "utf-8")
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="zju.edu.cn")
    if orig_msgid:
        msg["In-Reply-To"] = orig_msgid
        msg["References"] = " ".join(
            [r for r in (orig.get("References", "") + " " + orig_msgid).split() if r])
    msg.attach(MIMEText(body, "plain", "utf-8"))

    pwd = os.environ.get("ZJU_MAIL_PASS") or keychain_password()
    smtp_send(addr, pwd, msg, to_list, cc_list)
    out({"sent_from": addr, "to": to_list, "cc": cc_list,
         "in_reply_to": orig_msgid, "subject": str(msg["Subject"])})


def cmd_mark(args):
    ops = []
    if args.seen:
        ops.append(("+", "\\Seen"))
    if args.unseen:
        ops.append(("-", "\\Seen"))
    if args.flag:
        ops.append(("+", "\\Flagged"))
    if args.unflag:
        ops.append(("-", "\\Flagged"))
    for kw in args.keyword or []:
        ops.append(("+", kw))
    if not ops:
        fail("nothing to mark: pass --seen/--unseen/--flag/--unflag/--keyword")
    m, addr = imap_connect()
    select_folder(m, args.folder, readonly=False)
    applied = []
    for sign, flag in ops:
        typ, d = m.store(args.uid, f"{sign}FLAGS", flag)
        if typ != "OK":
            fail(f"store {sign}FLAGS {flag} failed: {d}")
        applied.append(f"{sign}{flag}")
    m.logout()
    out({"account": addr, "uid": args.uid, "folder": args.folder, "flags_applied": applied})


def cmd_draft(args):
    addr, _ = get_credentials()
    msg = build_mime(addr, args.to, args.cc, args.subject, args.body, [])
    m, _ = imap_connect()
    folder = args.folder or find_folder(m, "drafts", "草稿")
    if not folder:
        fail("draft folder not found: run `folders` and pass -f <name>")
    typ, d = m.append(utf7_encode(folder), r"(\Seen)", None, msg.as_bytes())
    if typ != "OK":
        fail(f"append to {folder} failed: {d}")
    uid = None
    for item in d:
        s = item.decode() if isinstance(item, bytes) else str(item)
        mm = re.search(r"APPENDUID \d+ (\d+)", s)
        if mm:
            uid = mm.group(1)
    m.logout()
    out({"account": addr, "saved_to": folder, "uid": uid,
         "to": args.to, "cc": args.cc, "subject": args.subject})


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(prog="zju_mail.py", description="ZJU mailbox wrapper (IMAP/SMTP)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("test")

    sub.add_parser("folders")

    sp = sub.add_parser("list")
    sp.add_argument("-f", "--folder", default="INBOX")
    sp.add_argument("-n", "--limit", type=int, default=10)
    sp.add_argument("--unread", action="store_true")
    sp.add_argument("--since", default=None, help="YYYY-MM-DD")

    sp = sub.add_parser("read")
    sp.add_argument("uid")
    sp.add_argument("-f", "--folder", default="INBOX")

    sp = sub.add_parser("search")
    sp.add_argument("query")
    sp.add_argument("-f", "--folder", default="INBOX")
    sp.add_argument("-n", "--limit", type=int, default=20)

    sp = sub.add_parser("attachments")
    sp.add_argument("uid")
    sp.add_argument("-f", "--folder", default="INBOX")
    sp.add_argument("-d", "--download", default=None, help="directory to save attachments")

    sp = sub.add_parser("send")
    sp.add_argument("--to", required=True, help="comma-separated recipients")
    sp.add_argument("--cc", default="", help="comma-separated cc")
    sp.add_argument("--subject", required=True)
    sp.add_argument("--body", required=True)
    sp.add_argument("--attach", nargs="*", default=[])

    sp = sub.add_parser("reply")
    sp.add_argument("uid")
    sp.add_argument("--body", required=True)
    sp.add_argument("-f", "--folder", default="INBOX")
    sp.add_argument("--all", action="store_true", help="reply-all (original To/Cc)")

    sp = sub.add_parser("draft")
    sp.add_argument("--to", default="", help="comma-separated recipients (optional)")
    sp.add_argument("--cc", default="", help="comma-separated cc")
    sp.add_argument("--subject", required=True)
    sp.add_argument("--body", required=True)
    sp.add_argument("-f", "--folder", default=None,
                    help="draft folder name (auto-detected: Drafts/草稿箱)")

    sp = sub.add_parser("mark")
    sp.add_argument("uid")
    sp.add_argument("-f", "--folder", default="INBOX")
    sp.add_argument("--seen", action="store_true")
    sp.add_argument("--unseen", action="store_true")
    sp.add_argument("--flag", action="store_true", help="set star/flagged")
    sp.add_argument("--unflag", action="store_true")
    sp.add_argument("--keyword", nargs="*", default=[],
                    help="custom IMAP keyword labels, e.g. --keyword 重要 Review")

    args = p.parse_args()
    if getattr(args, "since", None):
        d = email.utils.parsedate_to_datetime(args.since) if not re.match(r"^\d{4}-\d{2}-\d{2}$", args.since) else None
        if d is None:
            import datetime
            d = datetime.date.fromisoformat(args.since)
        args.since = d.strftime("%d-%b-%Y")
    if getattr(args, "to", None) and isinstance(args.to, str):
        args.to = [a.strip() for a in args.to.split(",") if a.strip()]
    if getattr(args, "cc", None) and isinstance(args.cc, str):
        args.cc = [a.strip() for a in args.cc.split(",") if a.strip()]

    {"test": cmd_test, "folders": cmd_folders, "list": cmd_list,
     "read": cmd_read, "search": cmd_search, "attachments": cmd_attachments,
     "send": cmd_send, "reply": cmd_reply, "mark": cmd_mark,
     "draft": cmd_draft}[args.cmd](args)


if __name__ == "__main__":
    main()
