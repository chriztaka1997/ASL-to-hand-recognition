import { Component, OnInit } from '@angular/core';
import * as M from 'materialize-css';

@Component({
  selector: 'app-authentication',
  templateUrl: './authentication.component.html',
  styleUrls: ['./authentication.component.scss']
})
export class AuthenticationComponent implements OnInit {
  constructor() {}

  ngOnInit() {
    const tabs = document.querySelector('.tabs');
    M.Tabs.init(tabs, {});
  }
}
