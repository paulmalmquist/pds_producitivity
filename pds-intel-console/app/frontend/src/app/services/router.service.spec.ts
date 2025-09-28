import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterService } from './router.service';

describe('RouterService', () => {
  let service: RouterService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule]
    });
    service = TestBed.inject(RouterService);
  });

  it('should classify analytics intents', () => {
    expect(service.classifyIntent('Show me a chart of costs')).toBe('analytics');
  });

  it('should classify tasks intents', () => {
    expect(service.classifyIntent('Create a Jira ticket for blockers')).toBe('tasks');
  });

  it('should detect mixed intents', () => {
    expect(service.classifyIntent('Summarize progress and create a Jira action')).toBe('mixed');
  });
});
