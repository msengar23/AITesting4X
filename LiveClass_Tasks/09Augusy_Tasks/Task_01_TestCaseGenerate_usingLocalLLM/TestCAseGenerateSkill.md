# VWO Login Dashboard Test Cases


| **Test ID** | **Description** | **Pre-conditions** | **Steps** | **Expected Result** | **Priority** |
| --- | --- | --- | --- | --- | --- |
| LT1 | Successful login with valid credentials | User is not authenticated | Log in with valid email and password | Login successfully, redirect to dashboard | High |
| LT2 | Successful registration with valid credentials | User is not authenticated | Register for account and log in | Redirects to registration page and confirms account creation | High |
| LT3 | Successful registration with invalid credentials | User is authenticated | Register for account and log in | Displays error message and redirects to login page | Medium |
| LT4 | Successful registration with password reset | User is not authenticated | Reset password and log in | Login successfully, redirects to password reset page | High |
| LT5 | Successful registration with forgotten password | User is not authenticated | Reset password and log in | Displays error message and redirects to password recovery page | Medium |
| LT6 | Successful registration with invalid email | User is authenticated | Register for account and log in | Displays error message and redirects to login page | Medium |
| LT7 | Successful registration with invalid password | User is authenticated | Register for account and log in | Displays error message and redirects to login page | Medium |
| LT8 | Successful registration with invalid username | User is authenticated | Register for account and log in | Displays error message and redirects to login page | Medium |
| LT9 | Registration with MFA | User is authenticated | Log in with valid email and password, and enable MFA | Validates MFA credentials, displays MFA confirmation message | High |
| LT10 | Registration with MFA failed | User is not authenticated | Log in with valid email and password, and enable MFA | Displays error message and redirects to login page | High |
| LT11 | Login with MFA | User is not authenticated | Log in with valid email and password, and enable MFA | Validates MFA credentials, displays MFA confirmation message | High |
| LT12 | Login with MFA failed | User is not authenticated | Log in with valid email and password, and enable MFA | Displays error message and redirects to login page | High |
| LT13 | Login with MFA and SSO | User is not authenticated | Log in with valid email and password, and enable MFA and SSO | Validates SSO credentials, displays SSO confirmation message | High |
| LT14 | Login with MFA and SSO failed | User is not authenticated | Log in with valid email and password, and enable MFA and SSO | Displays error message and redirects to login page | High |
| LT15 | Error handling with invalid email | User is authenticated | Log in with invalid email | Displays error message and redirects to login page | Medium |
| LT16 | Error handling with invalid password | User is authenticated | Log in with invalid password | Displays error message and redirects to login page | Medium |
| LT17 | Error handling with password reset | User is not authenticated | Reset password and log in | Displays error message and redirects to password recovery page | Medium |
| LT18 | Error handling with forgotten password | User is not authenticated | Reset password and log in | Displays error message and redirects to password recovery page | Medium |
| LT19 | Error handling with invalid username | User is authenticated | Log in with invalid username | Displays error message and redirects to login page | Medium |
| LT20 | Error handling with invalid password (repeated attempt) | User is authenticated | Reset password and log in | Displays error message and redirects to password recovery page | Medium |
| LT21 | Security audit with login | User is not authenticated | Conduct security audit, including login and error handling | Validates security audit results | Low |
| LT22 | Security audit with error handling | User is not authenticated | Conduct security audit, including login and error handling | Validates security audit results | Low |
| LT23 | Security audit with MFA | User is not authenticated | Conduct security audit, including login and MFA | Validates security audit results | Low |
| LT24 | Security audit with SSO | User is not authenticated | Conduct security audit, including login and SSO | Validates security audit results | Low |
| LT25 | Security audit with MFA and SSO | User is not authenticated | Conduct security audit, including login, MFA, and SSO | Validates security audit results | Low |
| LT26 | Performance testing with login | User is not authenticated | Complete login process, including password reset and account linking | Completes login process and confirms account linking | Low |
| LT27 | Performance testing with password reset | User is not authenticated | Reset password and log in | Completes login process and confirms account linking | Low |
| LT28 | Performance testing with account linking | User is not authenticated | Link account to other services, including Google and Microsoft | Completes login process and confirms account linking | Low |
| LT29 | Performance testing with MFA | User is not authenticated | Log in with valid email and password, and enable MFA | Validates MFA credentials, displays MFA confirmation message | High |
| LT30 | Performance testing with SSO | User is not authenticated | Log in with valid email and password, and enable SSO | Validates SSO credentials, displays SSO confirmation message | High |
