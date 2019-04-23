import { Component, OnInit } from '@angular/core';
import { UsersService } from 'src/app/services/users.service';
import _ from 'lodash';
import { TokenService } from 'src/app/services/token.service';
import io from 'socket.io-client';

@Component({
  selector: 'app-people',
  templateUrl: './people.component.html',
  styleUrls: ['./people.component.scss']
})
export class PeopleComponent implements OnInit {
  socket: any;
  users = [];
  loggedInUser: any;
  userArr = [];
  constructor(private usersService: UsersService, private tokenService: TokenService) {
    this.socket = io.connect('http://localhost:3000');
  }

  ngOnInit() {
    // act as temp value to get the ccurrent user who is logged in
    this.loggedInUser = this.tokenService.GetPayload();
    this.GetUsers();
    this.GetUserById();

    this.socket.on('refreshPage', data => {
      this.GetUsers();
      this.GetUserById();
    });
  }

  GetUsers() {
    this.usersService.GetAllUsers().subscribe(data => {
      _.remove(data.result, { username: this.loggedInUser.username });
      this.users = data.result;
    });
  }

  GetUserById() {
    this.usersService.GetUserByID(this.loggedInUser._id).subscribe(data => {
      this.userArr = data.result.following;
    });
  }

  GetUserByName() {
    this.usersService.GetUserByNAME(this.loggedInUser.username).subscribe(data => {
      console.log(data);
    });
  }

  FollowUser(user) {
    this.usersService.FollowUser(user._id).subscribe(data => {
      this.socket.emit('refresh', {});
    });
  }

  CheckInArray(arr, id) {
    const result = _.find(arr, ['userFollowed._id', id]);
    if (result) {
      return true;
    } else {
      return false;
    }
  }
}
