import { type Page } from '@playwright/test';
import { LoginPage } from './LoginPage';

export class PageFactory {
  constructor(private readonly page: Page) {}

  get loginPage(): LoginPage {
    return new LoginPage(this.page);
  }
}
