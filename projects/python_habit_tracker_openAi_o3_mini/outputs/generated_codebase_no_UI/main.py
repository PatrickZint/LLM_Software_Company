import argparse
from database import init_db
import habit_manager
import visualization
import exporter


def main():
    parser = argparse.ArgumentParser(description='Habit Tracking Application')
    subparsers = parser.add_subparsers(dest='command')

    # Sub-command: init
    parser_init = subparsers.add_parser('init', help='Initialize the database')

    # Sub-command: create habit
    parser_create = subparsers.add_parser('create', help='Create a new habit')
    parser_create.add_argument('--title', required=True, help='Title of the habit')
    parser_create.add_argument('--description', default='', help='Description of the habit')
    parser_create.add_argument('--goal', required=True, help='Goal details')
    parser_create.add_argument('--schedule', required=True, help='Schedule details (e.g., daily, Mon,Wed,Fri)')
    parser_create.add_argument('--start_date', required=True, help='Start date (YYYY-MM-DD)')
    parser_create.add_argument('--end_date', help='Optional end date (YYYY-MM-DD)')
    parser_create.add_argument('--category', default='', help='Category or tag for the habit')

    # Sub-command: log completion
    parser_log = subparsers.add_parser('log', help='Log habit completion')
    parser_log.add_argument('--habit_id', type=int, required=True, help='ID of the habit')
    parser_log.add_argument('--log_date', required=True, help='Date of completion (YYYY-MM-DD)')
    parser_log.add_argument('--status', default='completed', help='Status (e.g., completed)')
    parser_log.add_argument('--notes', default='', help='Optional notes for this log')

    # Sub-command: visualize
    parser_vis = subparsers.add_parser('visualize', help='Visualize habit progress')
    parser_vis.add_argument('--habit_id', type=int, required=True, help='ID of the habit to visualize')
    parser_vis.add_argument('--type', choices=['bar', 'line'], default='bar', help='Type of chart')

    # Sub-command: export
    parser_exp = subparsers.add_parser('export', help='Export habit data to CSV')
    parser_exp.add_argument('--filepath', required=True, help='Path to export CSV file')
    parser_exp.add_argument('--habit_id', type=int, help='Optional: export data for a specific habit')

    args = parser.parse_args()

    if args.command == 'init':
        init_db()
        print('Database initialized.')

    elif args.command == 'create':
        habit_id = habit_manager.create_habit(
            title=args.title,
            description=args.description,
            goal=args.goal,
            schedule=args.schedule,
            start_date=args.start_date,
            end_date=args.end_date,
            category=args.category
        )
        print(f'Habit created with ID: {habit_id}')

    elif args.command == 'log':
        log_id = habit_manager.log_habit_completion(
            habit_id=args.habit_id,
            log_date=args.log_date,
            status=args.status,
            notes=args.notes
        )
        print(f'Habit log created with ID: {log_id}')

    elif args.command == 'visualize':
        if args.type == 'bar':
            visualization.plot_habit_progress(args.habit_id)
        else:
            visualization.plot_habit_progress_line(args.habit_id)

    elif args.command == 'export':
        exporter.export_habit_data(filepath=args.filepath, habit_id=args.habit_id)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
