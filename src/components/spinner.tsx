import React from 'react';
import Loader from 'react-loader-spinner';

interface ISpinner {
  size: number;
  color: string;
  timeout?: number; // in secs
}

export const Spinner: React.FC<ISpinner> = ({ size, color, timeout }) => (
  <Loader type="Puff" color={color} height={size} width={size} timeout={timeout} />
);
