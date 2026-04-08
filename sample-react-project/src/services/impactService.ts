/*
 * Copyright IBM 2026
 * Licensed under the Apache License, Version 2.0
 */

export const getImpactMetrics = (audience: string): string[] => {
  const metricMap: Record<string, string[]> = {
    engineers: [
      'faster PR learning',
      'stronger policy awareness',
      'better AI code hygiene'
    ],
    leaders: [
      'visible adoption signals',
      'repeatable governance',
      'higher trust in AI delivery'
    ]
  };

  return metricMap[audience] || metricMap.engineers;
};

export const getUnusedMetricStory = (): string => {
  return 'Unused helper created intentionally for analyzer coverage.';
};

// Made with Bob
