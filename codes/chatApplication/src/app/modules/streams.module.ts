import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StreamsComponent } from '../components/streams/streams.component';
import { TokenService } from '../services/token.service';
import { ToolbarComponent } from '../components/toolbar/toolbar.component';
import { SideComponent } from '../components/side/side.component';
import { PeopleComponent } from '../components/people/people.component';
import { StreamsRoutingModule } from './streams-routing.module';
import { SettingsComponent } from '../components/settings/settings.component';

@NgModule({
  declarations: [StreamsComponent, ToolbarComponent, SideComponent, PeopleComponent, SettingsComponent],
  imports: [CommonModule, StreamsRoutingModule],
  exports: [StreamsComponent],
  providers: [TokenService]
})
export class StreamsModule {}
