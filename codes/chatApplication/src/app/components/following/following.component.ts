import { Component, OnInit } from '@angular/core';
import { TokenService } from 'src/app/services/token.service';
import { UsersService } from 'src/app/services/users.service';

@Component({
  selector: 'app-following',
  templateUrl: './following.component.html',
  styleUrls: ['./following.component.scss']
})
export class FollowingComponent implements OnInit {
  following = [];
  user: any;

  constructor(private tokenService: TokenService, private userService: UsersService) {}

  ngOnInit() {
    // This is always important step to get the current logged user information
    this.user = this.tokenService.GetPayload();
    this.GetUser();
  }

  GetUser() {
    this.userService.GetUserByID(this.user._id).subscribe(
      data => {
        this.following = data.result.following;
      },
      err => console.log(err)
    );
  }
}
