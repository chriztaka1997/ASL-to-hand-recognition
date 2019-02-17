import { Component, ViewChild } from '@angular/core';
import {WebcamImage} from 'ngx-webcam';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'ARTT';
  public handleImage(WebcamImage: WebcamImage){
    
  }
  

};


