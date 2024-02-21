__all__ = ["get_leaderboard"]


import numpy as np
import pandas as pd

from chaiverse.utils import get_submissions, distribute_to_workers
from chaiverse.metrics.feedback_metrics import get_metrics_from_feedback
from chaiverse.metrics.submission_metrics import get_metrics_from_submission
from chaiverse import constants, feedback


def get_leaderboard(
        developer_key=None,
        max_workers=constants.DEFAULT_MAX_WORKERS,
        submission_date_range=None,
        evaluation_date_range=None,
        submission_ids=None,
        fetch_feedback=False,
        ):
    submissions = get_submissions(developer_key, submission_date_range)
    submissions = _fill_submissions_with_default_values(submissions)
    submissions = _filter_submissions_by_submission_ids(submissions, submission_ids) if submission_ids != None else submissions
    submissions = _filter_submissions_by_feedback_count(submissions, constants.PUBLIC_LEADERBOARD_MINIMUM_FEEDBACK_COUNT)
    df = distribute_to_workers(
        get_leaderboard_row,
        submissions.items(),
        developer_key=developer_key,
        evaluation_date_range=evaluation_date_range,
        max_workers=max_workers,
        fetch_feedback=fetch_feedback
    )
    df = pd.DataFrame(df)
    if len(df):
        df.index = np.arange(1, len(df)+1)
    return df


def get_leaderboard_row(submission_item, developer_key=None, evaluation_date_range=None, fetch_feedback=False):
    submission_id, submission_data = submission_item
    if fetch_feedback:
        submission_data = _fill_submission_with_feedback_metrics(submission_id, submission_data, evaluation_date_range, developer_key)
    metrics = get_metrics_from_submission(submission_data) 
    submission = {'submission_id': submission_id, **submission_data, **metrics}
    return submission


def _fill_submissions_with_default_values(submissions):
    submissions = {
        submission_id: _fill_submission_with_default_values(submission_id, submission_data)
        for submission_id, submission_data in submissions.items()
    }
    return submissions


def _fill_submission_with_default_values(submission_id, submission_data):
    constant_field_defaults = constants.SUBMISSION_CONSTANT_FIELD_DEFAULTS
    custom_field_defaults = _get_custom_field_defaults(submission_id, submission_data)
    submission = {
        **constant_field_defaults,
        **custom_field_defaults,
        **submission_data
    }
    return submission


def _fill_submission_with_feedback_metrics(submission_id, submission_data, evaluation_date_range, developer_key=None):
    feedback_metrics = {}
    submission_feedback_total = submission_data['double_thumbs_up'] + submission_data['thumbs_up'] + submission_data['thumbs_down']
    is_updated = feedback.is_submission_updated(submission_id, submission_feedback_total)
    feedback_metrics = get_metrics_from_feedback(
        submission_id, 
        developer_key, 
        reload=is_updated, 
        evaluation_date_range=evaluation_date_range
    )
    submission_data = {**submission_data, **feedback_metrics}
    return submission_data


def _get_custom_field_defaults(submission_id, submission):
    custom_field_defaults = {
        'model_name': submission_id
    }
    return custom_field_defaults


def _filter_submissions_by_submission_ids(submissions, submission_ids):
    filtered_submissions = {
        submission_id: data
        for submission_id, data in submissions.items()
        if submission_id in submission_ids
    }
    return filtered_submissions


def _filter_submissions_by_feedback_count(submissions, min_feedback_count):
    submissions = {
        submission_id: submission_data for submission_id, submission_data in submissions.items()
        if submission_data.get('double_thumbs_up', 0) + submission_data['thumbs_up'] + submission_data['thumbs_down'] >= min_feedback_count
    }
    return submissions
