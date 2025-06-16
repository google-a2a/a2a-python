import unittest
import uuid

from unittest.mock import patch

from a2a.types import Message, Part, Role, TextPart
from a2a.utils.task import completed_task, new_task


class TestTask(unittest.TestCase):
    def test_new_task_status(self):
        message = Message(
            role=Role.user,
            parts=[Part(root=TextPart(text='test message'))],
            message_id=str(uuid.uuid4()),
        )
        task = new_task(message)
        self.assertEqual(task.status.state.value, 'submitted')

    @patch('uuid.uuid4')
    def test_new_task_generates_ids(self, mock_uuid4):
        mock_uuid = uuid.UUID('12345678-1234-5678-1234-567812345678')
        mock_uuid4.return_value = mock_uuid
        message = Message(
            role=Role.user,
            parts=[Part(root=TextPart(text='test message'))],
            message_id=str(uuid.uuid4()),
        )
        task = new_task(message)
        self.assertEqual(task.id, str(mock_uuid))
        self.assertEqual(task.context_id, str(mock_uuid))

    def test_new_task_uses_provided_ids(self):
        task_id = str(uuid.uuid4())
        context_id = str(uuid.uuid4())
        message = Message(
            role=Role.user,
            parts=[Part(root=TextPart(text='test message'))],
            message_id=str(uuid.uuid4()),
            task_id=task_id,
            context_id=context_id,
        )
        task = new_task(message)
        self.assertEqual(task.id, task_id)
        self.assertEqual(task.context_id, context_id)

    def test_new_task_initial_message_in_history(self):
        message = Message(
            role=Role.user,
            parts=[Part(root=TextPart(text='test message'))],
            message_id=str(uuid.uuid4()),
        )
        task = new_task(message)
        self.assertEqual(len(task.history), 1)
        self.assertEqual(task.history[0], message)

    def test_completed_task_status(self):
        task_id = str(uuid.uuid4())
        context_id = str(uuid.uuid4())
        artifacts = []  # Artifacts should be of type Artifact
        task = completed_task(
            task_id=task_id,
            context_id=context_id,
            artifacts=artifacts,
            history=[],
        )
        self.assertEqual(task.status.state.value, 'completed')

    def test_completed_task_assigns_ids_and_artifacts(self):
        task_id = str(uuid.uuid4())
        context_id = str(uuid.uuid4())
        artifacts = []  # Artifacts should be of type Artifact
        task = completed_task(
            task_id=task_id,
            context_id=context_id,
            artifacts=artifacts,
            history=[],
        )
        self.assertEqual(task.id, task_id)
        self.assertEqual(task.context_id, context_id)
        self.assertEqual(task.artifacts, artifacts)

    def test_completed_task_empty_history_if_not_provided(self):
        task_id = str(uuid.uuid4())
        context_id = str(uuid.uuid4())
        artifacts = []  # Artifacts should be of type Artifact
        task = completed_task(
            task_id=task_id, context_id=context_id, artifacts=artifacts
        )
        self.assertEqual(task.history, [])

    def test_completed_task_uses_provided_history(self):
        task_id = str(uuid.uuid4())
        context_id = str(uuid.uuid4())
        artifacts = []  # Artifacts should be of type Artifact
        history = [
            Message(
                role=Role.user,
                parts=[Part(root=TextPart(text='Hello'))],
                message_id=str(uuid.uuid4()),
            ),
            Message(
                role=Role.agent,
                parts=[Part(root=TextPart(text='Hi there'))],
                message_id=str(uuid.uuid4()),
            ),
        ]
        task = completed_task(
            task_id=task_id,
            context_id=context_id,
            artifacts=artifacts,
            history=history,
        )
        self.assertEqual(task.history, history)


if __name__ == '__main__':
    unittest.main()
