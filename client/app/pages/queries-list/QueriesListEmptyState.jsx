import React from 'react';
import PropTypes from 'prop-types';
import { BigMessage } from '@/components/BigMessage';
import { NoTaggedObjectsFound } from '@/components/NoTaggedObjectsFound';
import { EmptyState } from '@/components/empty-state/EmptyState';

export default function QueriesListEmptyState({ page, searchTerm, selectedTags }) {
  if (searchTerm !== '') {
    return (
      <BigMessage message="未查询到任何相关数据。" icon="fa-search" />
    );
  }
  if (selectedTags.length > 0) {
    return (
      <NoTaggedObjectsFound objectType="queries" tags={selectedTags} />
    );
  }
  switch (page) {
    case 'favorites': return (
      <BigMessage message="将指标标记为收藏以在此处列出。" icon="fa-star" />
    );
    case 'archive': return (
      <BigMessage message="回收的查询将在此处列出。" icon="fa-archive" />
    );
    case 'my': return (
      <div className="tiled bg-white p-15">
        <a href="queries/new" className="btn btn-primary btn-sm">Create your first query</a>
        {' '}to populate My Queries list. Need help? Check out our{' '}
        <a href="https://redash.io/help/user-guide/querying/writing-queries">query writing documentation</a>.
      </div>
    );
    default: return (
      <EmptyState
        icon="fa fa-code"
        illustration="query"
        description="组件化分析"
        helpLink=""
      />
    );
  }
}

QueriesListEmptyState.propTypes = {
  page: PropTypes.string.isRequired,
  searchTerm: PropTypes.string.isRequired,
  selectedTags: PropTypes.array.isRequired, // eslint-disable-line react/forbid-prop-types
};
