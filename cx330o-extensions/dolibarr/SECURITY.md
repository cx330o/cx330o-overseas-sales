# Security Policy

## Supported Versions

Security reports are valid on the current stable version and the development branch.

## Reporting a Vulnerability

To report a vulnerability:

- Send your report to admin@cx330o.com with a clear textual description of the report along with steps to reproduce the issue. Include attachments such as screenshots or proof of concept code as necessary.
- Do 1 report only per vulnerability.

## Responsible Disclosure

We are happy to thank everyone who submits valid reports which help us improve the security of the project.

You must be the first reporter of the vulnerability (duplicate reports are closed).

You must avoid tests that could cause degradation or interruption of our service.

You must not leak, manipulate, or destroy any user data of third parties to find your vulnerability.

## Scope

The scope covers the web application (backoffice) and the APIs.

### Qualified Vulnerabilities

* Remote code execution (RCE)
* Local files access and manipulation (LFI, RFI, XXE, SSRF, XSPA)
* Code injections (JS, SQL, PHP)
* Cross-Site Scripting (XSS)
* Cross-Site Requests Forgery (CSRF) with real security impact
* Open redirect
* Broken authentication & session management
* Insecure direct object references (IDOR)
* Horizontal and vertical privilege escalation

### Non-Qualified Vulnerabilities

* "Self" XSS
* Clickjacking/UI redressing
* Presence of autocomplete attribute on web forms
* Reports from automated web vulnerability scanners that have not been validated
* SSL/TLS practices
* Physical or social engineering attempts

Thank you for helping keep our project secure!
