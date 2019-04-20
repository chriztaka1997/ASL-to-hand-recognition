import { Component, OnInit } from '@angular/core';
import { UsersService } from 'src/app/services/users.service';
import _ from 'lodash';
import { TokenService } from 'src/app/services/token.service';

@Component({
  selector: 'app-people',
  templateUrl: './people.component.html',
  styleUrls: ['./people.component.scss']
})
export class PeopleComponent implements OnInit {
  users = [];
  loggedInUser: any;
  constructor(private usersService: UsersService, private tokenService: TokenService) {}

  ngOnInit() {
    // act as temp value to get the ccurrent user who is logged in
    this.loggedInUser = this.tokenService.GetPayload();
    console.log(this.loggedInUser.username);
    this.GetUsers();
  }

  GetUsers() {
    this.usersService.GetAllUsers().subscribe(data => {
      _.remove(data.result, { username: this.loggedInUser.username });
      this.users = data.result;
    });
  }
}
