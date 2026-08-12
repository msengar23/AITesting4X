Role -> You are a QA automation tester with 5 years of experience, You have a very good understanding of IT, and  projects like (https://app.wingify.com/#/login). You need to create test cases and a advance Playwright framework with Type Script,POM, Fixtures, hooks. it should be enterprise-level framework that we need to create.



I  -> Instructions

- Generate a Complete advance playwright testcases and Frameworks with Type script following the standard of enterprise level standards.
- Automate and verify the results of the login page [https://app.wingify.com/#/login], ensure that UI is thoroughly tested with valid and invalid testcases.
- [Critical] - Apply the Fixtures, hooks and others and necessary setup/teardown logic.
- [Critical] Implement robust exception handling within both Page Object model and test file spec.ts using structured test.describe with test and for credential use session storage function through process.env file (make template for .env file). Add Alure report in Package.cofig page. 
- [Mandatory] Use Page Object Model with  constructor initialization, and reusable functions. 
- [Mandatory] - It is important that you use only Playwright locators and xpath . 
- [Output] - - Output only runnable code, no explanations, comments, dependencies, or extra text. 
- [Don't] - Don't use the css selectors, ID, name and others things.
- [Don't] - Don't add comments and other bad coding practice.
- [Generate] - Generate the 2 scripts only with the valid and invalid testcases of the login page.
- [Don't Use] Hardcoded credential for login
- Maintain a consistent structure, readability, and modularity across all generated scripts.




C -> Context
You are creating a login page scripts with proper framework for the https://app.wingify.com/#/login login, which is a AB Testing website with valid and invalid login page where in the login page you have the email, password and Sign in button with Forgot Password,  remember me functionalities, Other authentication links like Google, using SSO, using Passkey. 



**E -> Example**
Example structure for Page Factory Pattern:

typescript

// pages/LoginPage.ts

import { type Locator, type Page } from '@playwright/test';

export class LoginPage {
  private readonly usernameInput: Locator;
  private readonly passwordInput: Locator;
  private readonly loginButton: Locator;

  constructor(private page: Page) {
    this.usernameInput = page.locator('#username');
    this.passwordInput = page.locator('#password');
    this.loginButton = page.locator('button[type="submit"]');
  }

  async navigate() {
    await this.page.goto('/login');
  }

  async login(user: string, pass: string) {
    await this.usernameInput.fill(user);
    await this.passwordInput.fill(pass);
    await this.loginButton.click();
  }
}



// pages/PageFactory.ts
import { type Page } from '@playwright/test';
import { LoginPage } from './LoginPage';

export class PageFactory {
  constructor(private page: Page) {}

  get loginPage(): LoginPage {
    return new LoginPage(this.page);
  }

 
**P -> PARAMETERS**
with production level automation script expert with pin point accuracy and almost zero bad coding practice. 

-  I have external URLs, external staging URLs. I will give you the external username and password as well 


O -> Output
Provide only: 

- 1 Page Object file (.ts) 
- 2 test file spec.ts
 3 Allure report for test execution
- Fixture
- .env file 
- hooks
- No explanations or additional content.


T -> Tone 
Technical, precisely, enterprise-grade, code-one.

