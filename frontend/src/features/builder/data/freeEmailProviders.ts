/**
 * Free Email Providers - Phase 1
 * 
 * List of common free email providers that are blocked when
 * "Business Email Only" validation is enabled.
 */

export const FREE_EMAIL_PROVIDERS = [
    // Major providers
    'gmail.com',
    'googlemail.com',
    'yahoo.com',
    'yahoo.co.uk',
    'yahoo.fr',
    'yahoo.de',
    'hotmail.com',
    'hotmail.co.uk',
    'hotmail.fr',
    'hotmail.de',
    'outlook.com',
    'outlook.co.uk',
    'live.com',
    'live.co.uk',
    'msn.com',
    'aol.com',
    'aol.co.uk',
    'icloud.com',
    'me.com',
    'mac.com',
    
    // Privacy-focused
    'proton.me',
    'protonmail.com',
    'tutanota.com',
    'tutamail.com',
    
    // Regional providers
    'mail.com',
    'email.com',
    'usa.com',
    'gmx.com',
    'gmx.net',
    'gmx.de',
    'web.de',
    'freenet.de',
    'yandex.com',
    'yandex.ru',
    'mail.ru',
    'inbox.ru',
    'bk.ru',
    'list.ru',
    'qq.com',
    '163.com',
    '126.com',
    'sina.com',
    'sohu.com',
    'naver.com',
    'hanmail.net',
    'daum.net',
    'rediffmail.com',
    
    // Other common free providers
    'zoho.com',
    'zohomail.com',
    'fastmail.com',
    'hushmail.com',
    'runbox.com',
    'mailfence.com',
    'posteo.de',
    'mailbox.org',
    'disroot.org',
    'riseup.net',
    'cock.li',
    'airmail.cc',
];

/**
 * Check if an email domain is a free email provider
 */
export function isFreeEmailProvider(email: string): boolean {
    const domain = email.split('@')[1]?.toLowerCase();
    if (!domain) return false;
    return FREE_EMAIL_PROVIDERS.includes(domain);
}

/**
 * Get the domain from an email address
 */
export function getEmailDomain(email: string): string | null {
    const match = email.match(/@([^@]+)$/);
    return match ? match[1].toLowerCase() : null;
}

export default FREE_EMAIL_PROVIDERS;

