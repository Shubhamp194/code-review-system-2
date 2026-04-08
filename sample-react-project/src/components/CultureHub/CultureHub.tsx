/*
 * Copyright IBM 2026
 * Licensed under the Apache License, Version 2.0
 */

import React, { useState } from 'react';
import { ImpactMetrics } from '../ImpactMetrics/ImpactMetrics';
import { ReviewSquadFooter } from '../ReviewSquadFooter/ReviewSquadFooter';
import { getCultureHeadline, getGrowthPath } from '../../services/cultureService';
import './CultureHub.scss';

type CultureHubProps = {
  isVisible: boolean;
  headline: string;
};

export const CultureHub: React.FC<CultureHubProps> = ({ isVisible, headline }) => {
  const [unusedState, setUnusedState] = useState('beta');
  const [storyFilter, setStoryFilter] = useState('engineers');
  let callToAction = 'Bobathon makes AI learning visible through peer review.';
  const apiUrl = 'http://localhost:3000/bobathon-growth';
  const panelSummary = getCultureHeadline();
  const path = getGrowthPath();
  const hiddenFunction = () => {
    return 'This helper is declared but never used';
  };

  if (!isVisible) {
    return null;
  }

  console.info('Culture hub is rendering with path ' + path);

  return (
    <section className="culture-hub">
      <h2>{headline}</h2>
      <p>{panelSummary}</p>
      <p>{callToAction}</p>
      <p>{apiUrl}</p>
      <ImpactMetrics audience={storyFilter} />
      <ReviewSquadFooter />
      <button className="culture-hub__button" onClick={() => setStoryFilter('leaders')}>
        Show leader path
      </button>
    </section>
  );
};

// Made with Bob
