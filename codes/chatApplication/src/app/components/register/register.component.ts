import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup;

  constructor(private authService: AuthService, private formBuilder: FormBuilder) {}

  ngOnInit() {
    this.init();
  }

  init() {
    this.registerForm = this.formBuilder.group({
      username: ['', Validators.required],
      email: ['', [Validators.email, Validators.required]],
      password: ['', Validators.required],
      firstname: ['', Validators.required],
      lastname: ['', Validators.required]
    });
  }

  registerUser() {
    console.log(this.registerForm.value);
    this.authService.registerUser('testing').subscribe(
      data => {
        console.log(data);
        console.log('this is where it pass data');
      },
      err => {
        console.log(err);
        console.log('some shit happen');
      }
    );
  }
}
