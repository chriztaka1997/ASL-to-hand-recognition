import { Component, ViewChild } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'ARTT';
  @ViewChild('videoWebcam') videoWebcam: any;
  video: any;

  ngOnInit(){
    this.video = this.videoWebcam.nativeElement;
  }

  initCamera(config:any){
    var browser = <any>navigator;
    browser.getUserMedia = (browser.getUserMedia || browser.webkitGetUserMedia || browser.mozGetUserMedia || browser.msGetUserMedia);

    browser.mediaDevices.getUserMedia(config).then(stream => {
      this.video.src = window.URL.createObjectURL(stream);
      this.video.play();
    }).catch(function(err){
      console.log("Error: ", err);
    });
  }

};
export class CameraComponent{
  @ViewChild('videoWebcam') videoWebcam:any;

}

