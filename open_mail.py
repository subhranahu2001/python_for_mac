import os, time, json, threading, shutil, sys, tempfile, atexit, re
import urllib.request, urllib.parse, socket
import tkinter as tk
from tkinter import scrolledtext
import hashlib, secrets, base64, uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

LOGO_B64 = "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"

API_URL = 'http://admindata.cioreview.com/22_07_testing_/sumit_pass/get_credentials_multy.php'

# ── Tunables (timeouts in seconds) ────────────────────────────────
T_PAGE_LOAD     = 30   # max time to wait for any page to load
T_ELEMENT_WAIT  = 8    # max time waiting for a single element
T_LOGIN_TOTAL   = 45   # hard cap on total login time per account
T_API_FETCH     = 12   # API call timeout
T_RETRY_DELAY   = 1.5  # delay before retry

# ── State ─────────────────────────────────────────────────────────
_driver         = None
_drv_lock       = threading.Lock()
_tab_map        = {}
_gmail_idx      = {}
_cdm_path       = None
_blank_tab_used = False

def _cdm():
    global _cdm_path
    if not _cdm_path: _cdm_path = ChromeDriverManager().install()
    return _cdm_path

def _profile():
    p = os.path.join(os.path.expanduser('~'), 'mail_opener_profiles', f'inst_{os.getpid()}')
    os.makedirs(p, exist_ok=True); return p

def _build():
    o = webdriver.ChromeOptions()
    o.add_argument(f'--user-data-dir={_profile()}')
    o.add_argument('--profile-directory=Default')
    o.add_argument('--disable-blink-features=AutomationControlled')
    o.add_argument('--no-first-run'); o.add_argument('--no-default-browser-check')
    o.add_argument('--no-sandbox'); o.add_argument('--disable-dev-shm-usage')
    o.add_argument('--disable-extensions'); o.add_argument('--disable-popup-blocking')
    o.add_argument('--disable-infobars'); o.add_argument('--disable-sync')
    o.add_argument('--disable-save-password-bubble'); o.add_argument('--password-store=basic')
    o.add_argument('--remote-debugging-port=0'); o.add_argument('--start-maximized')
    # Performance: disable images for faster loading (optional - comment if you need to see images)
    # o.add_argument('--blink-settings=imagesEnabled=false')
    o.add_experimental_option('excludeSwitches',['enable-automation','enable-logging'])
    o.add_experimental_option('useAutomationExtension', False)
    o.add_experimental_option('detach', False)
    o.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
        'profile.password_manager_leak_detection': False,
        'profile.default_content_setting_values.notifications': 2,
        'signin.allowed': False, 'signin.allowed_on_next_startup': False,
    })
    o.page_load_strategy = 'eager'  # don't wait for all subresources
    log = os.path.join(os.path.expanduser('~'), 'mail_opener_profiles', f'cdm_{os.getpid()}.log')
    svc = Service(_cdm(), log_output=log)
    d = webdriver.Chrome(service=svc, options=o)
    d.set_page_load_timeout(T_PAGE_LOAD)
    d.set_script_timeout(10)
    d.execute_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
    d.maximize_window()
    return d

def _alive(d):
    try: _ = d.window_handles; return True
    except: return False

def drv():
    global _driver, _blank_tab_used
    if _driver and _alive(_driver): return _driver
    with _drv_lock:
        if _driver and _alive(_driver): return _driver
        _tab_map.clear(); _gmail_idx.clear(); _blank_tab_used = False
        _driver = _build()
    return _driver

def _use_blank(d):
    global _blank_tab_used
    if _blank_tab_used: return False
    try:
        if len(d.window_handles)==1 and d.current_url in ('about:blank','data:,','','chrome://new-tab-page/'):
            _blank_tab_used = True; return True
    except: pass
    return False

def _new_tab(url='about:blank'):
    d = drv(); before = set(d.window_handles)
    try:
        d.execute_script(f'window.open("{url}","_blank");')
    except WebDriverException:
        pass
    try: WebDriverWait(d,4).until(lambda x: len(x.window_handles)>len(before))
    except: pass
    new = set(d.window_handles)-before
    h = new.pop() if new else d.window_handles[-1]
    d.switch_to.window(h)
    return h

def tab_count():
    try: return len(drv().window_handles) if _alive(_driver) else 0
    except: return 0

def _cleanup():
    if not _driver or not _alive(_driver): return
    try:
        live = set(_driver.window_handles)
        dead = [k for k,h in _tab_map.items() if h not in live]
        for k in dead: del _tab_map[k]
    except: pass

# ── Page state helpers ────────────────────────────────────────────
def _visible_text(d, max_len=4000):
    try:
        return (d.execute_script("return document.body ? document.body.innerText : '';") or '')[:max_len]
    except:
        return ''

def _safe_get(d, url):
    """Navigate with timeout protection."""
    try:
        d.get(url)
        return True
    except TimeoutException:
        try: d.execute_script("window.stop();")
        except: pass
        return False
    except WebDriverException:
        return False

def _fill(d, el, text):
    try:
        d.execute_script("""
            var e=arguments[0],v=arguments[1];
            var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
            s.call(e,v);e.dispatchEvent(new Event('input',{bubbles:true}));
            e.dispatchEvent(new Event('change',{bubbles:true}));
        """, el, text)
    except:
        el.clear(); el.send_keys(text)

def _click_any(d, selectors, timeout=3):
    """Try each selector; click the first visible/clickable one. Returns True if clicked."""
    end = time.time() + timeout
    while time.time() < end:
        for by, sel in selectors:
            try:
                el = d.find_element(by, sel)
                if el.is_displayed() and el.is_enabled():
                    try:
                        el.click()
                    except:
                        d.execute_script("arguments[0].click();", el)
                    return True
            except:
                continue
        time.sleep(0.15)
    return False

def _wait_any(d, selectors, timeout=T_ELEMENT_WAIT):
    """Wait until any of the selectors is visible. Returns the matched (by,sel) or None."""
    end = time.time() + timeout
    while time.time() < end:
        for by, sel in selectors:
            try:
                el = d.find_element(by, sel)
                if el.is_displayed():
                    return (by, sel)
            except:
                continue
        time.sleep(0.15)
    return None

def _next(d):
    _click_any(d, [
        (By.ID, 'identifierNext'),
        (By.ID, 'passwordNext'),
        (By.XPATH, '//button[contains(.,"Next")]'),
        (By.XPATH, '//*[@id="idSIButton9"]'),
        (By.XPATH, '//input[@type="submit"]'),
        (By.XPATH, '//button[@type="submit"]'),
    ], timeout=2)

def _dismiss_quick(d):
    """Quick non-blocking dismiss of common popups. No long waits."""
    for t in ['No thanks', 'Not now', 'Skip', 'Never']:
        try:
            els = d.find_elements(By.XPATH, f'//*[normalize-space(text())="{t}"]')
            for el in els:
                if el.is_displayed():
                    try: d.execute_script("arguments[0].click();", el)
                    except: pass
                    return
        except: pass

# ── Gmail ─────────────────────────────────────────────────────────
def _gmail_inbox(d):
    try: return 'mail.google.com/mail' in d.current_url
    except: return False

def _gmail_email_step(d, email):
    """Enter email and click Next. Returns True if accepted."""
    f = _wait_any(d, [(By.CSS_SELECTOR, 'input[type="email"]')], timeout=T_ELEMENT_WAIT)
    if not f: return False
    try:
        el = d.find_element(*f)
        el.click(); _fill(d, el, email)
        if len((el.get_attribute('value') or '')) < max(1, len(email)//2):
            el.clear(); el.send_keys(email)
    except: return False
    _click_any(d, [
        (By.ID, 'identifierNext'),
        (By.XPATH, '//button[contains(.,"Next")]'),
    ], timeout=2)
    # Wait for transition (email field disappears OR password appears OR challenge)
    end = time.time() + 8
    while time.time() < end:
        try:
            cu = d.current_url
            if 'mail.google.com/mail' in cu: return True
            if d.find_elements(By.CSS_SELECTOR, 'input[type="password"]'):
                pw_field = d.find_element(By.CSS_SELECTOR, 'input[type="password"]')
                if pw_field.is_displayed(): return True
            # Check if email field is gone or shows error
            vtext = _visible_text(d, 2000)
            if "Couldn't find your" in vtext or "couldn't find" in vtext.lower():
                return False
        except: pass
        time.sleep(0.2)
    return True  # assume transition happened

def _gmail_password_step(d, pw):
    """Enter password and click Next. Returns True if inbox reached."""
    f = _wait_any(d, [(By.CSS_SELECTOR, 'input[type="password"]')], timeout=T_ELEMENT_WAIT)
    if not f: return _gmail_inbox(d)
    try:
        el = d.find_element(*f)
        el.click(); _fill(d, el, pw)
        if len((el.get_attribute('value') or '')) < max(1, len(pw)//2):
            el.clear(); el.send_keys(pw)
    except: pass
    _click_any(d, [
        (By.ID, 'passwordNext'),
        (By.XPATH, '//button[contains(.,"Next")]'),
    ], timeout=2)
    # Wait for inbox or challenge/error
    end = time.time() + 12
    while time.time() < end:
        if _gmail_inbox(d): return True
        cu = d.current_url
        vtext = _visible_text(d, 3000)
        if 'Wrong password' in vtext: return False
        if '/challenge/' in cu and '/challenge/pwd' not in cu: return False
        if 'gds.google.com' in cu: return False
        time.sleep(0.25)
    return _gmail_inbox(d)

def open_gmail(email, pw):
    _cleanup(); d = drv(); key = f'g:{email}'
    if key in _tab_map and _tab_map[key] in d.window_handles:
        d.switch_to.window(_tab_map[key]); return

    # If we already know the multi-account index, jump straight there
    if email in _gmail_idx:
        idx = _gmail_idx[email]
        url = f'https://mail.google.com/mail/u/{idx}/'
        if _use_blank(d): _safe_get(d, url)
        else: _new_tab(url)
        try: WebDriverWait(d, 5).until(lambda x: 'mail.google.com' in x.current_url)
        except: pass
        if _gmail_inbox(d):
            _tab_map[key] = d.current_window_handle
            return
        # Index was stale; fall through to full login

    # Full login flow
    qe = urllib.parse.quote(email)
    base = ('https://accounts.google.com/signin/v2/identifier' if not _gmail_idx
            else 'https://accounts.google.com/AddSession')
    url = f'{base}?continue=https://mail.google.com/mail/&service=mail&Email={qe}'

    if _use_blank(d): _safe_get(d, url)
    else: _new_tab(url)

    start = time.time()

    # Hard cap on overall login time
    def _check_timeout():
        if time.time() - start > T_LOGIN_TOTAL:
            raise RuntimeError('Gmail: Login timed out (page too slow)')

    # Wait for any meaningful state to appear
    matched = _wait_any(d, [
        (By.CSS_SELECTOR, 'input[type="email"]'),
        (By.CSS_SELECTOR, 'input[type="password"]'),
        (By.XPATH, '//*[contains(text(),"Choose an account")]'),
        (By.XPATH, '//*[contains(text(),"mail.google.com")]'),
    ], timeout=10)

    _check_timeout()

    if _gmail_inbox(d):
        pass  # Already logged in via cookies
    else:
        # Handle "Choose an account" page
        vtext = _visible_text(d, 3000)
        if 'Choose an account' in vtext:
            clicked = False
            for sel in [f'//*[@data-email="{email}"]',
                        f'//*[@data-identifier="{email}"]',
                        f'//*[contains(@data-email,"{email}")]',
                        f'//div[contains(text(),"{email}")]']:
                try:
                    el = d.find_element(By.XPATH, sel)
                    if el.is_displayed():
                        d.execute_script("arguments[0].click();", el)
                        clicked = True; break
                except: continue
            if not clicked:
                _click_any(d, [
                    (By.XPATH, '//*[contains(text(),"Use another account")]'),
                    (By.XPATH, '//*[contains(text(),"Add account")]'),
                ], timeout=2)
            _wait_any(d, [(By.CSS_SELECTOR, 'input[type="email"]'),
                          (By.CSS_SELECTOR, 'input[type="password"]')], timeout=5)

        _check_timeout()

        # Email step (if email field is visible)
        try:
            ef = d.find_element(By.CSS_SELECTOR, 'input[type="email"]')
            if ef.is_displayed():
                if not _gmail_email_step(d, email):
                    vtext = _visible_text(d, 3000)
                    if "couldn't find" in vtext.lower() or "Couldn't find" in vtext:
                        raise RuntimeError("Gmail: Couldn't find account")
                    raise RuntimeError('Gmail: Email entry failed')
        except RuntimeError: raise
        except: pass

        _check_timeout()

        # Password step (if password field is visible)
        if not _gmail_inbox(d):
            try:
                pf = d.find_element(By.CSS_SELECTOR, 'input[type="password"]')
                if pf.is_displayed():
                    if not _gmail_password_step(d, pw):
                        cu = d.current_url
                        vtext = _visible_text(d, 4000)
                        if 'Wrong password' in vtext:
                            raise RuntimeError('Gmail: Wrong password')
                        if '2-Step Verification' in vtext or 'authenticator' in vtext.lower():
                            raise RuntimeError('Gmail: 2-Step Verification required')
                        if 'Verify your phone' in vtext or 'verification code' in vtext.lower():
                            raise RuntimeError('Gmail: Phone verification required')
                        if 'recovery email' in vtext.lower():
                            raise RuntimeError('Gmail: Recovery email verification')
                        if "Confirm you're not a robot" in vtext or 'captcha' in vtext.lower():
                            raise RuntimeError('Gmail: CAPTCHA required')
                        if '/challenge/' in cu and '/challenge/pwd' not in cu:
                            raise RuntimeError('Gmail: Login challenge detected')
                        raise RuntimeError('Gmail: Login did not reach inbox')
            except RuntimeError: raise
            except: pass

        _check_timeout()

        # Final check
        if not _gmail_inbox(d):
            # Wait a tiny bit more in case the redirect is slow
            end = time.time() + 5
            while time.time() < end:
                if _gmail_inbox(d): break
                time.sleep(0.25)
            if not _gmail_inbox(d):
                raise RuntimeError('Gmail: Login did not reach inbox')

    # Record index from URL
    m = re.search(r'/mail/u/(\d+)/', d.current_url)
    idx = int(m.group(1)) if m else len(_gmail_idx)
    _gmail_idx[email] = idx
    target = f'https://mail.google.com/mail/u/{idx}/'
    if not d.current_url.startswith(target):
        _safe_get(d, target)
    _tab_map[key] = d.current_window_handle

# ── Outlook ───────────────────────────────────────────────────────
def _ourl(email):
    cv = base64.urlsafe_b64encode(secrets.token_bytes(40)).decode().rstrip('=')
    cc = base64.urlsafe_b64encode(hashlib.sha256(cv.encode()).digest()).decode().rstrip('=')
    n = str(uuid.uuid4()); ri = str(uuid.uuid4()); si = str(uuid.uuid4())
    st = base64.urlsafe_b64encode(
        json.dumps({"id": si, "meta": {"interactionType": "redirect"}}).encode()
    ).decode().rstrip('=')
    p = {'client_id': '9199bf20-a13f-4107-85dc-02114787ef48',
         'scope': 'https://outlook.office.com/.default openid profile offline_access',
         'redirect_uri': 'https://outlook.office365.com/mail/',
         'client-request-id': ri,
         'response_mode': 'fragment', 'client_info': '1', 'nonce': n, 'state': st,
         'response_type': 'code', 'code_challenge': cc, 'code_challenge_method': 'S256',
         'x-client-SKU': 'msal.js.browser', 'x-client-VER': '4.14.0',
         'login_hint': email, 'prompt': 'select_account'}
    return 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?' + urllib.parse.urlencode(p)

def _outlook_inbox(d):
    try:
        u = d.current_url
        return any(x in u for x in [
            'outlook.office365.com/mail', 'outlook.live.com/mail',
            'outlook.office.com/mail', 'outlook.cloud.microsoft/mail'])
    except: return False

def _outlook_pick(d, email):
    """Handle 'Pick an account' page."""
    vtext = _visible_text(d, 2000)
    if 'Pick an account' not in vtext: return
    local = email.split('@')[0].lower()
    dom = email.split('@')[-1][:10].lower()
    selectors = [
        f'//*[@data-test-id="{email}"]',
        f'//*[contains(@data-test-id,"{email}")]',
        f'//*[contains(@data-test-id,"{local}")]',
        f'//*[contains(@aria-label,"{email}")]',
        f'//small[contains(text(),"{local}@")]/../..',
        f'//div[contains(@class,"table") and contains(.,"{local}") and contains(.,"{dom}")]',
    ]
    clicked = False
    for sel in selectors:
        try:
            for el in d.find_elements(By.XPATH, sel):
                t = (el.text or '').lower()
                if 'use another' in t or 'pick an' in t: continue
                if el.is_displayed():
                    d.execute_script("arguments[0].click();", el)
                    clicked = True; break
            if clicked: break
        except: continue
    if not clicked:
        _click_any(d, [
            (By.XPATH, '//*[contains(text(),"Use another account")]'),
            (By.XPATH, '//*[contains(text(),"Sign in with a different account")]'),
        ], timeout=2)

def _outlook_pw(d, pw):
    """Enter password and submit."""
    matched = _wait_any(d, [
        (By.XPATH, '//input[@name="passwd"]'),
        (By.ID, 'i0118'),
        (By.CSS_SELECTOR, 'input[type="password"]'),
    ], timeout=T_ELEMENT_WAIT)
    if not matched: return False
    try:
        el = d.find_element(*matched)
        # Wait until clickable
        end = time.time() + 4
        while time.time() < end:
            try:
                if el.is_enabled() and el.is_displayed(): break
            except: pass
            time.sleep(0.15)
        el.click(); _fill(d, el, pw)
        if len((el.get_attribute('value') or '')) < max(1, len(pw)//2):
            el.clear(); el.send_keys(pw)
        _click_any(d, [
            (By.XPATH, '//button[text()="Next"]'),
            (By.XPATH, '//*[@id="idSIButton9"]'),
            (By.XPATH, '//input[@type="submit"]'),
        ], timeout=2)
        return True
    except:
        return False

def open_outlook(email, pw):
    _cleanup(); d = drv(); key = f'o:{email}'

    if key in _tab_map and _tab_map[key] in d.window_handles:
        d.switch_to.window(_tab_map[key]); return

    if _use_blank(d): _safe_get(d, _ourl(email))
    else: _new_tab(_ourl(email))
    _tab_map[key] = d.current_window_handle

    start = time.time()
    def _check_timeout():
        if time.time() - start > T_LOGIN_TOTAL:
            raise RuntimeError('Outlook: Login timed out (page too slow)')

    # Wait for any login state
    _wait_any(d, [
        (By.XPATH, '//*[contains(text(),"Pick an account")]'),
        (By.ID, 'i0116'),
        (By.XPATH, '//input[@name="passwd"]'),
        (By.ID, 'i0118'),
    ], timeout=10)

    _check_timeout()
    if _outlook_inbox(d): return

    # Handle "Pick an account"
    if 'Pick an account' in _visible_text(d, 2000):
        _outlook_pick(d, email)
        _wait_any(d, [(By.ID, 'i0116'), (By.XPATH, '//input[@name="passwd"]')], timeout=5)

    _check_timeout()
    if _outlook_inbox(d): return

    # Email step (i0116 may be pre-filled via login_hint)
    try:
        el = d.find_element(By.ID, 'i0116')
        if el.is_displayed():
            val = (el.get_attribute('value') or '').strip().lower()
            if val != email.lower():
                el.clear(); el.click(); _fill(d, el, email)
            _next(d)
            _wait_any(d, [(By.XPATH, '//input[@name="passwd"]'), (By.ID, 'i0118')], timeout=5)
    except: pass

    _check_timeout()
    if _outlook_inbox(d): return

    # Password step
    _outlook_pw(d, pw)

    # KMSI "Stay signed in?" prompt
    try:
        _click_any(d, [
            (By.XPATH, '//*[@id="idSIButton9"]'),
            (By.XPATH, '//button[text()="Yes"]'),
            (By.XPATH, '//button[text()="No"]'),
        ], timeout=3)
    except: pass

    # Wait for inbox or challenge
    end = time.time() + 12
    while time.time() < end:
        _check_timeout()
        if _outlook_inbox(d): break
        cu = d.current_url.lower()
        if '/proofs/' in cu or '/sa/' in cu: break
        time.sleep(0.25)

    if _outlook_inbox(d): return

    # Error classification
    cu = d.current_url.lower()
    vtext = _visible_text(d, 4000)

    if '/proofs/' in cu or '/sa/' in cu:
        if 'authenticator' in vtext.lower() or 'Approve sign in' in vtext:
            raise RuntimeError('Outlook: Authenticator approval required')
        if 'Enter the code we sent' in vtext or 'Verify your phone' in vtext:
            raise RuntimeError('Outlook: Phone/code verification required')
        raise RuntimeError('Outlook: Identity verification required')

    errors = [
        ('Your account or password is incorrect', 'Wrong password'),
        ('password is incorrect', 'Wrong password'),
        ("That Microsoft account doesn't exist", 'Account does not exist'),
        ("account doesn't exist", 'Account does not exist'),
        ('Your account has been locked', 'Account locked'),
        ('has been locked', 'Account locked'),
        ('Approve sign in request', 'Authenticator approval required'),
        ('Enter the code we sent to', 'Code verification required'),
        ('Verify your identity', 'Identity verification required'),
        ('More information required', 'More info required'),
    ]
    for tag, msg in errors:
        if tag in vtext:
            raise RuntimeError(f'Outlook: {msg}')

    # Fallback navigation
    _safe_get(d, 'https://outlook.office365.com/mail/')
    end = time.time() + 5
    while time.time() < end:
        if _outlook_inbox(d): return
        time.sleep(0.25)
    _safe_get(d, 'https://outlook.live.com/mail/')
    end = time.time() + 5
    while time.time() < end:
        if _outlook_inbox(d): return
        time.sleep(0.25)
    raise RuntimeError('Outlook: Login did not reach inbox')

# ── API ───────────────────────────────────────────────────────────
def _lip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]; s.close(); return ip
    except: return 'unknown'

def _gip():
    for u in ['https://api.ipify.org', 'https://checkip.amazonaws.com']:
        try:
            return urllib.request.urlopen(
                urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}),
                timeout=5).read().decode().strip()
        except: pass
    return 'unknown'

_ips = {}
def fetch(sid):
    global _ips
    if not _ips: _ips = {'li': _lip(), 'gi': _gip()}
    try:
        raw = urllib.request.urlopen(urllib.request.Request(
            f'{API_URL}?{urllib.parse.urlencode({"newpassword": sid.strip(), "local_ip": _ips["li"], "global_ip": _ips["gi"]})}'
        ), timeout=T_API_FETCH).read().decode()
    except Exception as e:
        raise RuntimeError(f'API: {e}')
    try:
        data = json.loads(raw)
    except:
        raise RuntimeError(f'Bad response: {raw[:60]}')
    if not data.get('email'): raise RuntimeError('Email not found')
    if not data.get('password'): raise RuntimeError('Password not found')
    return data

# ═══════════════════════════════════════════════════════════════════
# GUI
# ═══════════════════════════════════════════════════════════════════
root = tk.Tk(); root.title('Mail Opener'); root.geometry('400x580')
root.resizable(False, False); root.configure(bg='#f0f2f8')
root.eval('tk::PlaceWindow . center')

try: _logo = tk.PhotoImage(data=LOGO_B64)
except: _logo = None

card = tk.Frame(root, bg='white', highlightthickness=1, highlightbackground='#c8d0e4')
card.pack(padx=18, pady=18, fill='both', expand=True)
inner = tk.Frame(card, bg='white'); inner.pack(padx=20, pady=(0, 12), fill='both', expand=True)

if _logo: tk.Label(inner, image=_logo, bg='white').pack(pady=(0, 4))
tk.Label(inner, text='Enter Sender IDs to open mail', font=('Segoe UI', 10, 'bold'), bg='white').pack(pady=(0, 6))
tk.Frame(inner, bg='#e0e6f0', height=1).pack(fill='x', pady=(0, 10))

cv = tk.StringVar(value='gmail')

class Radio(tk.Frame):
    def __init__(self, p, txt, var, val):
        super().__init__(p, bg='white', cursor='hand2'); self.var = var; self.val = val; S = 18
        self.c = tk.Canvas(self, width=S, height=S, bg='white', highlightthickness=0, cursor='hand2')
        self.c.pack(side='left', padx=(0, 5))
        lbl = tk.Label(self, text=txt, font=('Segoe UI', 11, 'bold'), bg='white', cursor='hand2')
        lbl.pack(side='left')
        for w in (self.c, lbl, self): w.bind('<Button-1>', lambda _: self.var.set(self.val))
        var.trace_add('write', lambda *_: self._draw()); self._draw()

    def _draw(self):
        c = self.c; c.delete('all'); S = 18
        c.create_oval(1, 1, S-1, S-1, outline='#000', width=2)
        if self.var.get() == self.val:
            c.create_oval(4, 4, S-4, S-4, fill='#000', outline='#000')

rf = tk.Frame(inner, bg='white'); rf.pack(pady=(2, 10))
Radio(rf, 'Gmail', cv, 'gmail').pack(side='left', padx=18)
Radio(rf, 'Outlook', cv, 'outlook').pack(side='left', padx=18)

tk.Label(inner, text='Sender IDs  (one per line)', font=('Segoe UI', 9, 'bold'), bg='white', fg='#333').pack(anchor='w')
txt = scrolledtext.ScrolledText(inner, font=('Segoe UI', 10), height=10,
    relief='solid', bd=1, bg='white', fg='#111', wrap=tk.WORD, insertbackground='#333')
txt.pack(fill='both', expand=True, pady=(3, 0))
txt.focus()

br = tk.Frame(inner, bg='white'); br.pack(fill='x', pady=(10, 0))
open_btn = tk.Button(br, text='▶  Open Mail', font=('Segoe UI', 11, 'bold'),
    bg='#4285F4', fg='white', relief='flat', cursor='hand2', pady=8,
    command=lambda: submit())
open_btn.pack(side='left', fill='x', expand=True, padx=(0, 6))
tk.Button(br, text='✕ Clear', font=('Segoe UI', 10), bg='#e8eaed', fg='#444',
    relief='flat', cursor='hand2', pady=8,
    command=lambda: [txt.delete('1.0', tk.END), txt.tag_remove('ok', '1.0', tk.END),
                     txt.tag_remove('err', '1.0', tk.END), txt.tag_remove('cur', '1.0', tk.END)]
).pack(side='left')

bot = tk.Frame(inner, bg='white'); bot.pack(fill='x', pady=(8, 0))
tab_lbl = tk.Label(bot, text='Tabs: 0', font=('Segoe UI', 9), bg='white', fg='#555'); tab_lbl.pack(side='left')
prog_lbl = tk.Label(bot, text='', font=('Segoe UI', 9, 'bold'), bg='white', fg='#1a73e8'); prog_lbl.pack(side='right')

sf = tk.Frame(inner, bg='white', height=26); sf.pack(fill='x'); sf.pack_propagate(False)
sl = tk.Label(sf, text='', font=('Segoe UI', 9, 'bold'), bg='white', fg='#1a73e8',
              wraplength=360, justify='left')
sl.pack(side='left', expand=True)

ef = tk.Frame(inner, bg='#fff0f0', bd=1, relief='solid')
el = tk.Label(ef, text='', font=('Segoe UI', 9), bg='#fff0f0', fg='#cc0000',
              wraplength=360, justify='left', padx=8, pady=5)
el.pack(anchor='w')

txt.tag_config('ok',  foreground='#0a6630', background='#f0fff4')
txt.tag_config('err', foreground='#cc0000', background='#fff0f0')
txt.tag_config('cur', background='#e8f0fe')

def show_err(m): el.config(text=f'⚠  {m}'); ef.pack(fill='x', pady=(4, 0))
def clr_err():   el.config(text=''); ef.pack_forget()
def status(t, c='#1a73e8'): sl.config(text=t, fg=c); clr_err()

def mark_line(sid, tag):
    content = txt.get('1.0', tk.END)
    for i, line in enumerate(content.split('\n'), start=1):
        if line.strip() == sid.strip():
            txt.tag_remove('ok',  f'{i}.0', f'{i}.end')
            txt.tag_remove('err', f'{i}.0', f'{i}.end')
            txt.tag_remove('cur', f'{i}.0', f'{i}.end')
            txt.tag_add(tag, f'{i}.0', f'{i}.end')
            txt.see(f'{i}.0')
            break

def mark_line_with_reason(sid, tag, reason):
    content = txt.get('1.0', tk.END)
    for i, line in enumerate(content.split('\n'), start=1):
        stripped = line.strip()
        # Match either the bare sid or "sid  ← reason"
        if stripped == sid.strip() or stripped.startswith(sid.strip() + '  \u2190 '):
            txt.tag_remove('ok',  f'{i}.0', f'{i}.end')
            txt.tag_remove('err', f'{i}.0', f'{i}.end')
            txt.tag_remove('cur', f'{i}.0', f'{i}.end')
            txt.delete(f'{i}.0', f'{i}.end')
            txt.insert(f'{i}.0', f'{sid}  \u2190 {reason}')
            txt.tag_add(tag, f'{i}.0', f'{i}.end')
            txt.see(f'{i}.0')
            break

def mark_current(sid):
    content = txt.get('1.0', tk.END)
    txt.tag_remove('cur', '1.0', tk.END)
    for i, line in enumerate(content.split('\n'), start=1):
        stripped = line.strip()
        if stripped == sid.strip() or stripped.startswith(sid.strip() + '  '):
            txt.tag_add('cur', f'{i}.0', f'{i}.end'); txt.see(f'{i}.0'); break

def refresh():
    tab_lbl.config(text=f'Tabs: {tab_count()}')
    root.after(2000, refresh)

# ── Error classification ─────────────────────────────────────────
def _classify_error(m):
    if m.startswith('Gmail: ') or m.startswith('Outlook: '):
        return m.split(': ', 1)[1]
    ml = m.lower()
    if 'Email not found' in m:    return 'ID not found in DB'
    if 'Password not found' in m: return 'Password missing in DB'
    if 'Bad response' in m:       return 'Invalid API response'
    if m.startswith('API:'):      return 'API error'
    if 'timeout' in ml or 'timed out' in ml: return 'Network timeout'
    if 'urlopen' in ml or 'connection' in ml: return 'API unreachable'
    if 'chrome' in ml or 'session' in ml:    return 'Browser crashed'
    if 'stale' in ml or 'no such element' in ml: return 'Page changed mid-login'
    return m[:80]

# Errors that should NOT be retried (definitive)
_NO_RETRY = [
    'wrong password', "couldn't find account", 'account not found',
    'account disabled', 'account suspended', 'account locked',
    'account does not exist', '2-step verification', 'phone verification',
    'authenticator approval', 'code verification', 'identity verification',
    'recovery email', 'captcha', 'more info required',
    'id not found in db', 'password missing in db',
]

def _is_definitive(reason):
    rl = reason.lower()
    return any(k in rl for k in _NO_RETRY)

def _close_failed_tab(email):
    """Close the tab for a failed login attempt so retry starts fresh."""
    try:
        d = drv()
        for prefix in ('g:', 'o:'):
            key = f'{prefix}{email}'
            if key in _tab_map:
                h = _tab_map.pop(key)
                if h in d.window_handles and len(d.window_handles) > 1:
                    try:
                        d.switch_to.window(h)
                        d.close()
                        d.switch_to.window(d.window_handles[-1])
                    except: pass
    except: pass

# ── Submit ────────────────────────────────────────────────────────
_running = threading.Event()
MAX_RETRIES = 2  # reduced from 3 - retrying definitive errors wastes time

def submit():
    if _running.is_set(): return
    raw_lines = [s.strip() for s in txt.get('1.0', tk.END).split('\n') if s.strip()]
    sids = []
    for line in raw_lines:
        if '  \u2190 ' in line:
            sids.append(line.split('  \u2190 ')[0].strip())
        else:
            sids.append(line)
    if not sids:
        show_err('Please enter at least one Sender ID.'); return
    client = cv.get()
    txt.tag_remove('ok', '1.0', tk.END)
    txt.tag_remove('err', '1.0', tk.END)
    txt.tag_remove('cur', '1.0', tk.END)
    clr_err(); _running.set()
    open_btn.config(state='disabled', bg='#a0b4d6', cursor='arrow', text='Running...')
    total = len(sids)

    def run_all():
        fn = open_gmail if client == 'gmail' else open_outlook
        ok_count = 0; fail_count = 0

        for i, sid in enumerate(sids):
            root.after(0, lambda s=sid: mark_current(s))
            root.after(0, lambda i=i, t=total, s=sid: [
                prog_lbl.config(text=f'{i+1} / {t}'),
                status(f'({i+1}/{t}) Fetching {s}...', '#1a73e8')
            ])

            # Step 1: fetch credentials
            try:
                res = fetch(sid)
                if res.get('status') != 'ok':
                    raise RuntimeError(res.get('error', 'Not found'))
                email = res['email']; pw = res['password']
            except Exception as ex:
                fail_count += 1
                reason = _classify_error(str(ex) or type(ex).__name__)
                root.after(0, lambda s=sid, r=reason: mark_line_with_reason(s, 'err', r))
                root.after(0, lambda s=sid, r=reason, i=i, t=total:
                    status(f'\u26a0 ({i+1}/{t}) {s} \u2192 {r}', '#cc0000'))
                continue

            # Step 2: login with retry (only for non-definitive errors)
            last_err = None
            for attempt in range(MAX_RETRIES):
                try:
                    lbl = f'({i+1}/{total}) Opening {email}...'
                    if attempt > 0:
                        lbl = f'({i+1}/{total}) Retry {attempt+1} {email}...'
                    root.after(0, lambda l=lbl: status(l, '#1a73e8'))
                    fn(email, pw)
                    last_err = None
                    break
                except Exception as ex:
                    last_err = ex
                    reason = _classify_error(str(ex) or type(ex).__name__)
                    if _is_definitive(reason):
                        break
                    if attempt < MAX_RETRIES - 1:
                        root.after(0, lambda e=email, i=i, t=total, r=reason:
                            status(f'({i+1}/{t}) Retrying {e} ({r})...', '#e37400'))
                        _close_failed_tab(email)
                        time.sleep(T_RETRY_DELAY)

            if last_err is None:
                ok_count += 1
                root.after(0, lambda s=sid: mark_line(s, 'ok'))
            else:
                fail_count += 1
                reason = _classify_error(str(last_err) or type(last_err).__name__)
                root.after(0, lambda s=sid, r=reason: mark_line_with_reason(s, 'err', r))
                root.after(0, lambda s=sid, r=reason, i=i, t=total:
                    status(f'\u26a0 ({i+1}/{t}) {s} \u2192 {r}', '#cc0000'))

        _running.clear()
        root.after(0, lambda: [
            status(f'\u2714 Done \u2014 {ok_count} opened, {fail_count} failed',
                   '#0a6630' if fail_count == 0 else '#e37400'),
            prog_lbl.config(text=f'{ok_count}/{total} \u2714'),
            open_btn.config(state='normal', bg='#4285F4', cursor='hand2', text='\u25b6  Open Mail')
        ])

    threading.Thread(target=run_all, daemon=True).start()

root.bind('<Control-Return>', lambda e: submit())

def _start():
    def _do():
        try:
            root.after(0, lambda: status('Starting Chrome...', '#aaaaaa'))
            _cdm(); drv()
            root.after(0, lambda: [
                status('\u2714 Ready \u2014 paste Sender IDs and click Open Mail', '#0a6630'),
                root.after(5000, clr_err)
            ])
        except Exception as e:
            m = str(e)
            root.after(0, lambda m=m: status(f'Error: {m}', '#cc0000'))
    threading.Thread(target=_do, daemon=True).start()

def _cleanup_profile():
    try: shutil.rmtree(_profile(), ignore_errors=True)
    except: pass
atexit.register(_cleanup_profile)

def _on_close():
    try:
        if _driver and _alive(_driver): _driver.quit()
    except: pass
    try: root.destroy()
    except: pass

root.protocol('WM_DELETE_WINDOW', _on_close)

refresh()
root.after(300, _start)
root.mainloop()