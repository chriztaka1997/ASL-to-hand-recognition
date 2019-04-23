import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthenticationComponent } from '../components/authentication/authentication.component';
import { LoginComponent } from '../components/login/login.component';
import { RegisterComponent } from '../components/register/register.component';
import { AuthService } from '../services/auth.service';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [AuthenticationComponent, LoginComponent, RegisterComponent],
  imports: [CommonModule, HttpClientModule, FormsModule, ReactiveFormsModule],
  exports: [AuthenticationComponent, LoginComponent, RegisterComponent],
  providers: [AuthService]
})
export class AuthModule {}
