import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
const baseURL = 'hhttp://localhost:3000/api/artt';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(private http: HttpClient) {}

  registerUser(body): Observable<any> {
    return this.http.post(`${baseURL}/register`, body);
  }
}
