import { render, screen } from '@testing-library/react';
import { vi } from 'vitest';
import App from '../App';

vi.stubGlobal('fetch', vi.fn(() => Promise.resolve({ ok: true }) as Response));

test('renders application heading', async () => {
  render(<App />);
  const heading = await screen.findByRole('heading', { name: /Survaize/i });
  expect(heading).toBeInTheDocument();
});
