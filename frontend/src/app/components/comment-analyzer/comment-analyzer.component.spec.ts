import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommentAnalyzerComponent } from './comment-analyzer.component';

describe('CommentAnalyzerComponent', () => {
  let component: CommentAnalyzerComponent;
  let fixture: ComponentFixture<CommentAnalyzerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CommentAnalyzerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CommentAnalyzerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
