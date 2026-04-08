/*
 * Copyright IBM 2026
 * Licensed under the Apache License, Version 2.0
 */

import React from 'react';
import { VisionPanel } from '../VisionPanel/VisionPanel';
import { CultureHub } from '../CultureHub/CultureHub';
import { getHomeStory, getUnsafeHtmlSnippet, unusedHomeHelper } from '../../services/homeService';
import './HomePage.scss';

export const HomePage: React.FC = () => {
  const squadLabel = 'Bob Review Squad';
  const story = getHomeStory();
  const htmlSnippet = getUnsafeHtmlSnippet();
  const unusedHeroMessage = 'This variable is intentionally unused for analyzer coverage';
  const [isBannerVisible, setIsBannerVisible] = React.useState(true);

  console.log('Rendering home page for Bobathon growth story');
  debugger;

  return (
    <main className="home-page">
      <header className="home-page__header">
        <h1>{squadLabel}</h1>
        <p>{story}</p>
      </header>

      <section
        className="home-page__intro"
        dangerouslySetInnerHTML={{ __html: htmlSnippet }}
      />

      <VisionPanel title="Why Bobathon matters" />

      <CultureHub
        isVisible={isBannerVisible}
        headline="How Bobathon builds AI culture inside IBM"
      />

      <button
        className="home-page__button"
        onClick={() => setIsBannerVisible(!isBannerVisible)}
      >
        Toggle AI culture story
      </button>
    </main>
  );
};

// Made with Bob
