import {render} from 'sentry-test/reactTestingLibrary';

import SentryDocumentTitle from './sentryDocumentTitle';

describe('SentryDocumentTitle', () => {
  it('sets the docuemnt title', () => {
    render(<SentryDocumentTitle title="This is a test" />);
    expect(document.title).toBe('This is a test — Sentinel');
  });

  it('adds a organization slug', () => {
    render(<SentryDocumentTitle orgSlug="org" title="This is a test" />);
    expect(document.title).toBe('This is a test — org — Sentinel');
  });

  it('adds a project slug', () => {
    render(<SentryDocumentTitle projectSlug="project" title="This is a test" />);
    expect(document.title).toBe('This is a test — project — Sentinel');
  });

  it('adds a organization and project slug', () => {
    render(
      <SentryDocumentTitle orgSlug="org" projectSlug="project" title="This is a test" />
    );
    expect(document.title).toBe('This is a test — org — project — Sentinel');
  });

  it('sets the title without suffix', () => {
    render(<SentryDocumentTitle title="This is a test" noSuffix />);
    expect(document.title).toBe('This is a test');
  });

  it('reverts to the parent title', () => {
    const {rerender} = render(
      <SentryDocumentTitle title="This is a test">
        <SentryDocumentTitle title="child title">Content</SentryDocumentTitle>
      </SentryDocumentTitle>
    );

    expect(document.title).toBe('child title — Sentinel');

    rerender(
      <SentryDocumentTitle title="This is a test">new Content</SentryDocumentTitle>
    );

    expect(document.title).toBe('This is a test — Sentinel');
  });
});
