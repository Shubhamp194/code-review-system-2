/*
 * Copyright IBM 2026
 * Licensed under the Apache License, Version 2.0
 */

import React from 'react';
import './ReviewSquadFooter.scss';

export const ReviewSquadFooter: React.FC = () => {
  const footerTitle = 'Bob Review Squad';
  const footerMessage =
    'Created by Sachin Chotwani & Shubham Pandey using BOB for IBM';

  return (
    <footer className="review-squad-footer">
      <h4>{footerTitle}</h4>
      <p>{footerMessage}</p>
    </footer>
  );
};

// Made with Bob
