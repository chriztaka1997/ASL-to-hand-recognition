import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { WebcamModule } from 'ngx-webcam';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthModule } from './modules/auth.module';
import { AuthRoutingModule } from './modules/auth-routing.module';

@NgModule({
  declarations: [AppComponent],
  imports: [BrowserModule, WebcamModule, AuthModule, AuthRoutingModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
