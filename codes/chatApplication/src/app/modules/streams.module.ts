import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StreamsComponent } from '../components/streams/streams.component';
import { TokenService } from '../services/token.service';
import { ToolbarComponent } from '../components/toolbar/toolbar.component';
import { SideComponent } from '../components/side/side.component';
import { PeopleComponent } from '../components/people/people.component';
import { StreamsRoutingModule } from './streams-routing.module';
import { SettingsComponent } from '../components/settings/settings.component';
import { UsersService } from '../services/users.service';
import { FollowingComponent } from '../components/following/following.component';
import { FollowersComponent } from '../components/followers/followers.component';
import { CharComponent } from '../components/char/char.component';
import { MessageComponent } from '../components/message/message.component';
import {MessageService} from '../services/message.service';
@NgModule({
  declarations: [StreamsComponent, ToolbarComponent, SideComponent, PeopleComponent, SettingsComponent, FollowingComponent, FollowersComponent, CharComponent, MessageComponent],
  imports: [CommonModule, StreamsRoutingModule],
  exports: [StreamsComponent],
  providers: [TokenService, UsersService, MessageService]
})
export class StreamsModule {}
