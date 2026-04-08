/*
 * Copyright IBM 2026
 * Licensed under the Apache License, Version 2.0
 */

import React from 'react';
import { fetchVisionSignals } from '../../services/visionService';
import './VisionPanel.scss';

type VisionPanelProps = {
  title: string;
};

export const VisionPanel: React.FC<VisionPanelProps> = ({ title }) => {
  let summary = 'Bobathon helps IBM teams turn AI curiosity into delivery habits.';
  var legacyCount = 3;
  const data = fetchVisionSignals();
  const unusedInsight = 'AI culture grows when review habits are consistent.';
  const htmlNote = '<strong>Unsafe HTML</strong>';

  return (
    <section className="vision-panel">
      <h2>{title}</h2>
      <p>{summary}</p>
      <p>
        {data.join(', ')} and {legacyCount} squad accelerators support AI adoption.
      </p>
      <div dangerouslySetInnerHTML={{ __html: htmlNote }} />
    </section>
  );
};

// Made with Bob
