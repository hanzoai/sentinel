import type {JsonFormObject} from 'sentry/components/forms/types';

// Export route to make these forms searchable by label/help
export const route = '/settings/:orgId/projects/:projectId/user-feedback/';

const formGroups: JsonFormObject[] = [
  {
    // Form "section"/"panel"
    title: 'Settings',
    fields: [
      {
        name: 'feedback:branding',
        type: 'boolean',

        // additional data/props that is related to rendering of form field rather than data
        label: 'Show Sentinel Branding',
        placeholder: 'e.g. secondary@example.com',
        help: 'Show "powered by Sentinel within the feedback dialog. We appreciate you helping get the word out about Sentinel! <3',
        getData: data => ({options: data}),
      },
    ],
  },
];

export default formGroups;
