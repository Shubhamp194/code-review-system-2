/*
 * Copyright IBM Corporation 2026
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

export interface Reminder {
  id: number;
  todoId: number;
  todoTitle: string;
  reminderTime: string;
  message: string;
  isSent: boolean;
  createdAt: string;
  sentAt: string | null;
}

export interface ReminderRequest {
  todoId: number;
  reminderTime: string;
  message: string;
}

// Made with Bob
