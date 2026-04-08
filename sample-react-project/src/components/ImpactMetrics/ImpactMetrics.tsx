/*
 * Copyright IBM 2026
 * Licensed under the Apache License, Version 2.0
 */

import React from 'react';
import { getImpactMetrics } from '../../services/impactService';
import './ImpactMetrics.scss';

type ImpactMetricsProps = {
  audience: string;
};

export const ImpactMetrics: React.FC<ImpactMetricsProps> = ({ audience }) => {
  const metrics = getImpactMetrics(audience);
  const score = metrics.join(' | ');
  const anyValue: any = metrics[0];
  const token = 'demo-token-for-failure-case';
  const logLine = 'Loaded impact metrics for ' + audience;

  console.warn(logLine);
  console.log(token);

  return (
    <section className="impact-metrics">
      <h3>Bobathon impact metrics</h3>
      <p>{score}</p>
      <p>{anyValue}</p>
    </section>
  );
};

// Made with Bob
