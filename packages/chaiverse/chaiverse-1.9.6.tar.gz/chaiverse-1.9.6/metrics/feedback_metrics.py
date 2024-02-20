__all__ = ["FeedbackMetrics"]


from collections import defaultdict
from typing import Optional

import numpy as np

from chaiverse.lib import date_tools
from chaiverse.feedback import get_feedback
from chaiverse.schemas import DateRange
from chaiverse.metrics.conversation_metrics import ConversationMetrics


class FeedbackMetrics():
    def __init__(self, feedback_data):
        feedback_dict = feedback_data['feedback']
        feedback_dict = _insert_server_epoch_time(feedback_dict)
        self.feedbacks = list(feedback_dict.values())

    def filter_duplicated_uid(self):
        self.feedbacks = _filter_duplicated_uid_feedbacks(self.feedbacks)

    def filter_for_date_range(self, evaluation_date_range: Optional[DateRange]):
        self.feedbacks = [
            feedback for feedback in self.feedbacks
            if date_tools.is_epoch_time_in_date_range(feedback['server_epoch_time'], evaluation_date_range)
        ]

    def calc_metrics(self):
        thumbs_up = self.thumbs_up
        double_thumbs_up = self.double_thumbs_up
        total_feedback_count = self.total_feedback_count
        metrics = {
            'mcl': self.mcl,
            'thumbs_up': thumbs_up,
            'thumbs_down': total_feedback_count - thumbs_up - double_thumbs_up,
            'double_thumbs_up': double_thumbs_up,
            'repetition': self.repetition_score,
        }
        return metrics

    @property
    def convo_metrics(self):
        return [ConversationMetrics(feedback['messages']) for feedback in self.feedbacks]

    @property
    def thumbs_up(self):
        thumbs_ups = [1 if feedback['thumbs_up'] == 1 else 0 for feedback in self.feedbacks]
        thumbs_up = sum(thumbs_ups)
        return thumbs_up

    @property
    def double_thumbs_up(self):
        double_thumbs_ups = [1 if feedback['thumbs_up'] == 2 else 0 for feedback in self.feedbacks]
        double_thumbs_up = sum(double_thumbs_ups)
        return double_thumbs_up

    @property
    def total_feedback_count(self):
        return len(self.feedbacks)

    @property
    def mcl(self):
        return np.mean([m.mcl for m in self.convo_metrics])

    @property
    def repetition_score(self):
        scores = np.array([m.repetition_score for m in self.convo_metrics])
        is_public = np.array([feedback.get('public', True) for feedback in self.feedbacks])
        return np.nanmean(scores[is_public]) if len(scores) else float('nan')


def _insert_server_epoch_time(feedback_dict):
    for feedback_id, feedback in feedback_dict.items():
        feedback['server_epoch_time'] = int(feedback_id.split('_')[-1])
    return feedback_dict


def _filter_duplicated_uid_feedbacks(feedbacks):
    user_feedbacks = defaultdict(list)
    for feedback in feedbacks:
        user_id = feedback["conversation_id"].split("_")[3]
        user_feedbacks[user_id].append(feedback)
    feedbacks = [metrics[0] for _, metrics in user_feedbacks.items()]
    return feedbacks


def get_metrics_from_feedback(submission_id, developer_key, reload=True, evaluation_date_range=None):
    feedback_data = get_feedback(submission_id, developer_key, reload=reload)
    feedback_metrics = FeedbackMetrics(feedback_data.raw_data)
    feedback_metrics.filter_for_date_range(evaluation_date_range)
    feedback_metrics.filter_duplicated_uid()
    metrics = feedback_metrics.calc_metrics()
    return metrics