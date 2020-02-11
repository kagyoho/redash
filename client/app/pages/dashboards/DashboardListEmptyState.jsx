import React from 'react';
import PropTypes from 'prop-types';
import { BigMessage } from '@/components/BigMessage';
import { NoTaggedObjectsFound } from '@/components/NoTaggedObjectsFound';
import { EmptyState } from '@/components/empty-state/EmptyState';

export default function DashboardListEmptyState({ page, searchTerm, selectedTags }) {
  if (searchTerm !== '') {
    return (
      <BigMessage message="未查询到任何相关数据。" icon="fa-search" />
    );
  }
  if (selectedTags.length > 0) {
    return (
      <NoTaggedObjectsFound objectType="dashboards" tags={selectedTags} />
    );
  }
  switch (page) {
    case 'favorites': return (
      <BigMessage message="收藏的看板，将在此处一一列出。" icon="fa-star" />
    );
    default: return (
      <EmptyState
        icon="zmdi zmdi-view-quilt"
        description="自助式探索"
        illustration="dashboard"
        helpLink=""
        showDashboardStep
      />
    );
  }
}

DashboardListEmptyState.propTypes = {
  page: PropTypes.string.isRequired,
  searchTerm: PropTypes.string.isRequired,
  selectedTags: PropTypes.array.isRequired, // eslint-disable-line react/forbid-prop-types
};
