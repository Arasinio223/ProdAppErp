import { render, screen } from '@testing-library/react';
import App from './App';

test('renders login screen', () => {
  render(<App />);
  const headingElement = screen.getByTestId('login-heading');
  expect(headingElement).toBeInTheDocument();
});
