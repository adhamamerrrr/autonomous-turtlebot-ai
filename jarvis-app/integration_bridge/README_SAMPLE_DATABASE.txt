Sample database flow
====================

The app now uses these Firestore collections:

1. students
   Document ID = student ID
   Example: students/20210045
   Fields: id, name, major, email, level

2. professors
   Document ID = professor key
   Fields: id, name, department, office, email, schedule[]
   Each schedule item has: day, start, end, location, activity, course

3. smoke_detections
   Robot/ML writes pending detections here.
   Security guard reviews them.

4. violations
   Only confirmed guard-approved violations are written here.
   Student accounts read only confirmed violations assigned to their student ID.

You can add the sample database from inside the app:
Security Guard account -> Robot Simulator -> Add Sample Students + Professors

Or from Python:
python integration_bridge/seed_sample_database.py --service-account serviceAccountKey.json
