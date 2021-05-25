import * as React from 'react';
import styled from 'styled-components';
import { error } from 'loglevel';

export interface ErrorBoundaryProps {
  scope?: string;
  additionalInfo?: any;
  noFallbackRender?: boolean;
  onError?: () => void;
  customMessage?: React.ReactNode;
}

export interface ErrorBoundaryState {
  hasError: boolean;
}

const Container = styled.div`
  display: flex;
  align-items: center;
  align-content: center;
  justify-items: center;
  justify-content: center;
  text-align: center;
`;

export default class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(e: unknown) {
    return { hasError: true };
  }

  componentDidCatch(e: unknown, info: unknown) {
    error(`Error boundary in ${this.props.scope}`, {
      additionalInfo: this.props.additionalInfo,
      e,
      info,
    });
    this.props.onError && this.props.onError();
  }

  render() {
    if (this.state.hasError) {
      if (!this.props.noFallbackRender) {
        const message = this.props.customMessage ? this.props.customMessage : 'Something went wrong';

        return (
          <Container className="error-boundary">
            <h1>{message}</h1>
          </Container>
        );
      }
      return null;
    } else {
      return this.props.children || null;
    }
  }
}
