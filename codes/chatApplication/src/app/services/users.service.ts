import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
const baseURL = 'http://localhost:3000/api/artt';
@Injectable({
  providedIn: 'root'
})
export class UsersService {
  constructor(private http: HttpClient) {}

  GetAllUsers(): Observable<any> {
    return this.http.get(`${baseURL}/users`);
  }

  GetUserByID(id): Observable<any> {
    return this.http.get(`${baseURL}/users/${id}`);
  }

  GetUserByNAME(username): Observable<any> {
    return this.http.get(`${baseURL}/users/${username}`);
  }

  FollowUser(id): Observable<any> {
    return this.http.post(`${baseURL}/follow-user`, {
      userFollowed: id
    });
  }
}
