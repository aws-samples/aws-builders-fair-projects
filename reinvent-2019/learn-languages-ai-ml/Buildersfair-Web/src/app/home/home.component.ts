import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TweenMax } from 'node_modules/gsap';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit() {
    this.animate();
  }

  animate(): void {
    TweenMax.fromTo('h1', 3, {x: 250}, {x: 0});
    TweenMax.fromTo('#p1', 2.4, {x: 300}, {x: 0});
    TweenMax.fromTo('#p2', 3.3, {x: 300}, {x: 0});
  }
  playGame() {
    this.router.navigateByUrl('/game');
  }

  playTrailer() {
    this.router.navigateByUrl('/trailer');
  }
}
