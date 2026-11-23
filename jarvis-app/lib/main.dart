import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

const Color nguMaroon = Color(0xFF970039);
const Color nguDarkMaroon = Color(0xFF650024);
const Color nguGold = Color(0xFFDBA540);
const Color bgColor = Color(0xFFF7F8FB);

final List<Map<String, dynamic>> sampleStudents = [
  {
    'id': '20210045',
    'name': 'Ahmed Mohamed',
    'major': 'CCAS',
    'email': '20210045@ngu.edu.eg',
    'level': 'Year 4',
  },
  {
    'id': '202201565',
    'name': 'Ahmed Sherif Kamal',
    'major': 'CCAS',
    'email': '202201565@ngu.edu.eg',
    'level': 'Year 4',
  },
  {
    'id': '20210087',
    'name': 'Mariam Adel',
    'major': 'Computer Engineering',
    'email': '20210087@ngu.edu.eg',
    'level': 'Year 3',
  },
  {
    'id': '20210112',
    'name': 'Omar Hany',
    'major': 'Electronics Engineering',
    'email': '20210112@ngu.edu.eg',
    'level': 'Year 3',
  },
  {
    'id': '20220031',
    'name': 'Nour Youssef',
    'major': 'Biomedical Informatics',
    'email': '20220031@ngu.edu.eg',
    'level': 'Year 2',
  },
];

final List<Map<String, dynamic>> sampleProfessors = [
  {
    'id': 'khaled_hassan',
    'name': 'Dr. Khaled Hassan',
    'department': 'CCAS - Robotics and Autonomous Systems',
    'office': 'Office Room C314 - Robotics Faculty Office',
    'email': 'khaled.hassan@ngu.edu.eg',
    'schedule': [
      {'day': 'Sunday', 'start': '09:00', 'end': '10:30', 'location': 'Lab Room R101 - Robotics Lab', 'activity': 'Robotics Lecture', 'course': 'ROB401'},
      {'day': 'Sunday', 'start': '11:00', 'end': '12:30', 'location': 'Lecture Room C203', 'activity': 'Mobile Robotics Tutorial', 'course': 'ROB401'},
      {'day': 'Monday', 'start': '10:00', 'end': '12:00', 'location': 'Lab Room ASL-2 - Autonomous Systems Lab', 'activity': 'Graduation Project Supervision', 'course': 'GP'},
      {'day': 'Tuesday', 'start': '12:00', 'end': '13:30', 'location': 'Lecture Room C105', 'activity': 'Navigation Systems Lecture', 'course': 'ROB420'},
      {'day': 'Wednesday', 'start': '09:00', 'end': '10:30', 'location': 'Lab Room R101 - Robotics Lab', 'activity': 'Robot Perception Lab', 'course': 'ROB430'},
      {'day': 'Thursday', 'start': '13:00', 'end': '15:00', 'location': 'Lab Room R101 - Robotics Lab', 'activity': 'Robotics Practical Session', 'course': 'ROB401'},
    ],
  },
  {
    'id': 'sara_nabil',
    'name': 'Dr. Sara Nabil',
    'department': 'Computer Engineering',
    'office': 'Office Room B203 - Computer Engineering Faculty Office',
    'email': 'sara.nabil@ngu.edu.eg',
    'schedule': [
      {'day': 'Sunday', 'start': '10:00', 'end': '11:30', 'location': 'Lecture Room B105', 'activity': 'Database Systems Lecture', 'course': 'CSE302'},
      {'day': 'Monday', 'start': '09:00', 'end': '10:30', 'location': 'Lab Room B214 - Software Lab', 'activity': 'Software Engineering Lab', 'course': 'CSE310'},
      {'day': 'Tuesday', 'start': '11:00', 'end': '12:30', 'location': 'Lecture Room B210', 'activity': 'Software Engineering Lecture', 'course': 'CSE310'},
      {'day': 'Wednesday', 'start': '12:00', 'end': '14:00', 'location': 'Lab Room B216 - Computer Lab 2', 'activity': 'Database Lab', 'course': 'CSE302'},
      {'day': 'Thursday', 'start': '09:00', 'end': '10:30', 'location': 'Lecture Room B106', 'activity': 'Advanced SQL Lecture', 'course': 'CSE408'},
    ],
  },
  {
    'id': 'mohamed_ali',
    'name': 'Dr. Mohamed Ali',
    'department': 'Electronics Engineering',
    'office': 'Office Room C305 - Electronics Faculty Office',
    'email': 'mohamed.ali@ngu.edu.eg',
    'schedule': [
      {'day': 'Sunday', 'start': '12:00', 'end': '14:00', 'location': 'Lab Room E201 - Electronics Lab', 'activity': 'Digital Communications Lab', 'course': 'ECE405'},
      {'day': 'Monday', 'start': '13:00', 'end': '14:30', 'location': 'Lecture Room C101', 'activity': 'Digital Communications Lecture', 'course': 'ECE405'},
      {'day': 'Tuesday', 'start': '09:00', 'end': '10:30', 'location': 'Lab Room S110 - Signals Lab', 'activity': 'Signals Practical', 'course': 'ECE210'},
      {'day': 'Wednesday', 'start': '10:30', 'end': '12:00', 'location': 'Lecture Room C209', 'activity': 'Signals Tutorial', 'course': 'ECE210'},
      {'day': 'Thursday', 'start': '11:00', 'end': '12:30', 'location': 'Lecture Room C101', 'activity': 'Wireless Communication Lecture', 'course': 'ECE430'},
    ],
  },
  {
    'id': 'mona_youssef',
    'name': 'Dr. Mona Youssef',
    'department': 'AI and Data Science',
    'office': 'Office Room B312 - AI Faculty Office',
    'email': 'mona.youssef@ngu.edu.eg',
    'schedule': [
      {'day': 'Sunday', 'start': '13:00', 'end': '15:00', 'location': 'Lab Room A301 - AI Lab', 'activity': 'Machine Learning Lab', 'course': 'AI301'},
      {'day': 'Monday', 'start': '11:00', 'end': '12:30', 'location': 'Lecture Room B107', 'activity': 'Machine Learning Lecture', 'course': 'AI301'},
      {'day': 'Tuesday', 'start': '14:00', 'end': '16:00', 'location': 'Lecture Room B107', 'activity': 'Deep Learning Lecture', 'course': 'AI410'},
      {'day': 'Wednesday', 'start': '09:00', 'end': '11:00', 'location': 'Lab Room A301 - AI Lab', 'activity': 'Computer Vision Practical', 'course': 'AI420'},
      {'day': 'Thursday', 'start': '12:00', 'end': '13:30', 'location': 'Lecture Room B309', 'activity': 'Data Science Seminar', 'course': 'AI390'},
    ],
  },
  {
    'id': 'omar_fathy',
    'name': 'Dr. Omar Fathy',
    'department': 'Networks and Cybersecurity',
    'office': 'Office Room A220 - Networks Faculty Office',
    'email': 'omar.fathy@ngu.edu.eg',
    'schedule': [
      {'day': 'Sunday', 'start': '11:00', 'end': '12:30', 'location': 'Lecture Room A110', 'activity': 'Computer Networks Lecture', 'course': 'NET301'},
      {'day': 'Monday', 'start': '12:00', 'end': '13:30', 'location': 'Lab Room N201 - Network Lab', 'activity': 'Routing Lab', 'course': 'NET301'},
      {'day': 'Tuesday', 'start': '10:00', 'end': '11:30', 'location': 'Lecture Room A112', 'activity': 'Cybersecurity Lecture', 'course': 'SEC320'},
      {'day': 'Wednesday', 'start': '13:00', 'end': '14:30', 'location': 'Lab Room S205 - Security Lab', 'activity': 'Cryptography Lab', 'course': 'SEC410'},
      {'day': 'Thursday', 'start': '09:00', 'end': '10:30', 'location': 'Lecture Room A110', 'activity': 'Network Security Lecture', 'course': 'SEC330'},
    ],
  },
];

Future<void> seedSampleStudents() async {
  final batch = FirebaseFirestore.instance.batch();
  for (final student in sampleStudents) {
    final id = student['id'].toString();
    batch.set(FirebaseFirestore.instance.collection('students').doc(id), student);
  }
  await batch.commit();
}

Future<void> seedSampleProfessors({bool resetCollection = true}) async {
  final professorsRef = FirebaseFirestore.instance.collection('professors');

  // Reset first so old test/demo professor documents do not appear twice in the dropdown.
  if (resetCollection) {
    final oldDocs = await professorsRef.get();
    if (oldDocs.docs.isNotEmpty) {
      final deleteBatch = FirebaseFirestore.instance.batch();
      for (final doc in oldDocs.docs) {
        deleteBatch.delete(doc.reference);
      }
      await deleteBatch.commit();
    }
  }

  final batch = FirebaseFirestore.instance.batch();
  for (final professor in sampleProfessors) {
    final id = professor['id'].toString();
    batch.set(professorsRef.doc(id), professor);
  }
  await batch.commit();
}

Future<void> seedSampleDatabase() async {
  await seedSampleStudents();
  await seedSampleProfessors();
}

int? parseTimeToMinutes(String value) {
  final parts = value.trim().split(':');
  if (parts.length != 2) return null;
  final hour = int.tryParse(parts[0]);
  final minute = int.tryParse(parts[1]);
  if (hour == null || minute == null) return null;
  if (hour < 0 || hour > 23 || minute < 0 || minute > 59) return null;
  return hour * 60 + minute;
}

bool isTimeInsideSlot(String time, String start, String end) {
  final t = parseTimeToMinutes(time);
  final s = parseTimeToMinutes(start);
  final e = parseTimeToMinutes(end);
  if (t == null || s == null || e == null) return false;
  return t >= s && t < e;
}


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(const NGUCampusAssistantApp());
}

class NGUCampusAssistantApp extends StatelessWidget {
  const NGUCampusAssistantApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NGU Campus Assistant',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: nguMaroon,
        scaffoldBackgroundColor: bgColor,
        colorScheme: ColorScheme.fromSeed(seedColor: nguMaroon),
        appBarTheme: const AppBarTheme(
          backgroundColor: nguMaroon,
          foregroundColor: Colors.white,
          centerTitle: true,
          elevation: 0,
        ),
      ),
      home: const LoginPage(),
    );
  }
}

// LOGIN PAGE

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  String selectedRole = 'Student';
  final idController = TextEditingController(text: '20210045');
  final nameController = TextEditingController(text: 'Ahmed Mohamed');

  @override
  void dispose() {
    idController.dispose();
    nameController.dispose();
    super.dispose();
  }

  void login() {
    if (selectedRole == 'Student') {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => StudentShell(
            studentId: idController.text.trim(),
            studentName: nameController.text.trim(),
          ),
        ),
      );
    } else {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => const SecurityShell(),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final isStudent = selectedRole == 'Student';

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(18),
          child: Column(
            children: [
              const SizedBox(height: 24),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [nguMaroon, nguDarkMaroon],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(26),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Center(
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(22),
                        child: Image.asset(
                          'assets/images/ngu_logo.png',
                          width: 128,
                          height: 128,
                          fit: BoxFit.cover,
                        ),
                      ),
                    ),
                    const SizedBox(height: 18),
                    const Text(
                      'NGU',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 42,
                        fontWeight: FontWeight.w900,
                        letterSpacing: 1,
                      ),
                    ),
                    SizedBox(height: 4),
                    Text(
                      'NEWGIZA University',
                      style: TextStyle(color: Colors.white70, fontSize: 15),
                    ),
                    SizedBox(height: 18),
                    Text(
                      'Campus Assistant',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 28,
                        fontWeight: FontWeight.w900,
                      ),
                    ),
                    SizedBox(height: 6),
                    Text(
                      'Information desk and security monitoring system powered by TurtleBot4.',
                      style: TextStyle(color: Colors.white70, height: 1.4),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 22),
              AppCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Sign in as',
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.w900),
                    ),
                    const SizedBox(height: 14),
                    Row(
                      children: [
                        Expanded(
                          child: RoleCard(
                            title: 'Student',
                            icon: Icons.school,
                            selected: selectedRole == 'Student',
                            onTap: () => setState(() => selectedRole = 'Student'),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: RoleCard(
                            title: 'Security Guard',
                            icon: Icons.security,
                            selected: selectedRole == 'Security Guard',
                            onTap: () => setState(() => selectedRole = 'Security Guard'),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 18),
                    if (isStudent) ...[
                      TextField(
                        controller: idController,
                        decoration: inputDecoration('Student ID'),
                      ),
                      const SizedBox(height: 12),
                      TextField(
                        controller: nameController,
                        decoration: inputDecoration('Student Name'),
                      ),
                    ] else ...[
                      TextField(
                        controller: nameController,
                        decoration: inputDecoration('Security Guard Name'),
                      ),
                    ],
                    const SizedBox(height: 18),
                    PrimaryButton(text: 'Login', onPressed: login),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class RoleCard extends StatelessWidget {
  final String title;
  final IconData icon;
  final bool selected;
  final VoidCallback onTap;

  const RoleCard({
    super.key,
    required this.title,
    required this.icon,
    required this.selected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      borderRadius: BorderRadius.circular(18),
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: selected ? nguMaroon.withOpacity(0.10) : Colors.white,
          borderRadius: BorderRadius.circular(18),
          border: Border.all(
            color: selected ? nguMaroon : const Color(0xFFECEEF3),
            width: selected ? 2 : 1,
          ),
        ),
        child: Column(
          children: [
            Icon(icon, color: selected ? nguMaroon : Colors.grey, size: 34),
            const SizedBox(height: 8),
            Text(
              title,
              textAlign: TextAlign.center,
              style: TextStyle(
                color: selected ? nguMaroon : Colors.black87,
                fontWeight: FontWeight.w900,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// STUDENT INTERFACE
// Student now only has:
// 1. Warnings
// 2. Professor Lookup

class StudentShell extends StatefulWidget {
  final String studentId;
  final String studentName;

  const StudentShell({
    super.key,
    required this.studentId,
    required this.studentName,
  });

  @override
  State<StudentShell> createState() => _StudentShellState();
}

class _StudentShellState extends State<StudentShell> {
  int selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    final pages = [
      StudentWarningsPage(studentId: widget.studentId, studentName: widget.studentName),
      const ProfessorLookupPage(),
    ];

    const titles = [
      'My Warnings',
      'Professor Lookup',
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text(titles[selectedIndex]),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const LoginPage()));
            },
          ),
        ],
      ),
      body: pages[selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedIndex,
        onDestinationSelected: (index) => setState(() => selectedIndex = index),
        indicatorColor: nguMaroon.withOpacity(0.14),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.warning_amber_outlined),
            selectedIcon: Icon(Icons.warning),
            label: 'Warnings',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_search_outlined),
            selectedIcon: Icon(Icons.person_search),
            label: 'Doctors',
          ),
        ],
      ),
    );
  }
}

// SECURITY GUARD INTERFACE
// Security guard now only has:
// 1. Security Dashboard
// 2. Robot Simulator

class SecurityShell extends StatefulWidget {
  const SecurityShell({super.key});

  @override
  State<SecurityShell> createState() => _SecurityShellState();
}

class _SecurityShellState extends State<SecurityShell> {
  int selectedIndex = 0;

  final pages = const [
    SecurityDashboardPage(),
    RobotSimulatorPage(),
  ];

  final titles = const [
    'Security Dashboard',
    'Robot Simulator',
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(titles[selectedIndex]),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const LoginPage()));
            },
          ),
        ],
      ),
      body: pages[selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedIndex,
        onDestinationSelected: (index) => setState(() => selectedIndex = index),
        indicatorColor: nguMaroon.withOpacity(0.14),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.shield_outlined),
            selectedIcon: Icon(Icons.shield),
            label: 'Security',
          ),
          NavigationDestination(
            icon: Icon(Icons.smart_toy_outlined),
            selectedIcon: Icon(Icons.smart_toy),
            label: 'Simulator',
          ),
        ],
      ),
    );
  }
}

// SECURITY DASHBOARD

class SecurityDashboardPage extends StatelessWidget {
  const SecurityDashboardPage({super.key});

  Future<void> markFalseAlarm(BuildContext context, String detectionId) async {
    await FirebaseFirestore.instance.collection('smoke_detections').doc(detectionId).update({
      'status': 'False Alarm',
      'reviewedAt': FieldValue.serverTimestamp(),
      'reviewDecision': 'false_alarm',
    });
    if (context.mounted) showSnack(context, 'Detection marked as false alarm. No student warning was created.');
  }

  Future<void> confirmViolation(
    BuildContext context,
    String detectionId,
    Map<String, dynamic> detection,
  ) async {
    final studentIdController = TextEditingController();

    final studentId = await showDialog<String>(
      context: context,
      builder: (dialogContext) {
        return AlertDialog(
          title: const Text('Confirm Smoking Violation'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Enter the student ID manually. The violation will only appear in that student account after confirmation.'),
              const SizedBox(height: 14),
              TextField(
                controller: studentIdController,
                keyboardType: TextInputType.text,
                decoration: inputDecoration('Student ID'),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(dialogContext),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: nguMaroon, foregroundColor: Colors.white),
              onPressed: () {
                final value = studentIdController.text.trim();
                if (value.isNotEmpty) Navigator.pop(dialogContext, value);
              },
              child: const Text('Confirm'),
            ),
          ],
        );
      },
    );

    if (studentId == null || studentId.isEmpty) return;

    final db = FirebaseFirestore.instance;
    final studentDoc = await db.collection('students').doc(studentId).get();

    if (!studentDoc.exists) {
      if (context.mounted) {
        showSnack(context, 'Student ID $studentId was not found. Add sample students first or enter a valid student ID.');
      }
      return;
    }

    final studentData = studentDoc.data() ?? {};
    final studentName = (studentData['name'] ?? 'Student $studentId').toString();
    final studentMajor = (studentData['major'] ?? '').toString();

    final detectionRef = db.collection('smoke_detections').doc(detectionId);
    final violationRef = db.collection('violations').doc();

    await db.runTransaction((transaction) async {
      transaction.set(violationRef, {
        'studentId': studentId,
        'studentName': studentName,
        'studentMajor': studentMajor,
        'violationType': 'Smoking',
        'location': detection['location'] ?? '-',
        'robotId': detection['robotId'] ?? '-',
        'confidence': detection['confidence'] ?? 0.0,
        'status': 'New',
        'source': 'Security Guard Confirmation',
        'confirmed': true,
        'sourceDetectionId': detectionId,
        'photoUrl': detection['photoUrl'] ?? detection['imageUrl'] ?? '',
        'photoBase64': detection['photoBase64'] ?? '',
        'timestamp': FieldValue.serverTimestamp(),
      });

      transaction.update(detectionRef, {
        'status': 'Confirmed Violation',
        'reviewDecision': 'true_violation',
        'assignedStudentId': studentId,
        'assignedStudentName': studentName,
        'createdViolationId': violationRef.id,
        'reviewedAt': FieldValue.serverTimestamp(),
      });
    });

    if (context.mounted) showSnack(context, 'Violation confirmed and assigned to $studentName ($studentId).');
  }

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
      stream: FirebaseFirestore.instance
          .collection('smoke_detections')
          .orderBy('timestamp', descending: true)
          .snapshots(),
      builder: (context, snapshot) {
        if (snapshot.hasError) return ErrorView(message: snapshot.error.toString());
        if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());

        final docs = snapshot.data!.docs;
        final pending = docs.where((d) => (d.data()['status'] ?? 'Pending Review') == 'Pending Review').toList();
        final confirmed = docs.where((d) => d.data()['status'] == 'Confirmed Violation').toList();
        final falseAlarms = docs.where((d) => d.data()['status'] == 'False Alarm').toList();

        return SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              const HeaderCard(
                title: 'Security Guard Review',
                subtitle: 'Robot smoke detections are pending until a guard confirms the student ID.',
                icon: Icons.security,
              ),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(child: StatCard(title: 'Pending', value: pending.length.toString(), color: nguGold, icon: Icons.pending_actions)),
                  const SizedBox(width: 10),
                  Expanded(child: StatCard(title: 'Confirmed', value: confirmed.length.toString(), color: Colors.green, icon: Icons.verified)),
                  const SizedBox(width: 10),
                  Expanded(child: StatCard(title: 'False', value: falseAlarms.length.toString(), color: Colors.purple, icon: Icons.block)),
                ],
              ),
              const SizedBox(height: 18),
              const SecurityStudentWarningSummary(),
              const SizedBox(height: 18),
              SectionTitle(title: 'Pending Smoke Detections', trailing: '${pending.length} pending'),
              if (pending.isEmpty)
                const EmptyCard(text: 'No pending smoke detections. Robot detections will appear here for guard review.')
              else
                ...pending.map((doc) {
                  return SmokeDetectionCard(
                    id: doc.id,
                    data: doc.data(),
                    onFalseAlarm: () => markFalseAlarm(context, doc.id),
                    onConfirmViolation: () => confirmViolation(context, doc.id, doc.data()),
                  );
                }),
              const SizedBox(height: 10),
              SectionTitle(title: 'Reviewed Smoke Detections', trailing: '${confirmed.length + falseAlarms.length} reviewed'),
              if (confirmed.isEmpty && falseAlarms.isEmpty)
                const EmptyCard(text: 'Reviewed detections will appear here after the guard confirms or rejects them.')
              else
                ...docs.where((d) => (d.data()['status'] ?? 'Pending Review') != 'Pending Review').map((doc) {
                  return SmokeDetectionCard(
                    id: doc.id,
                    data: doc.data(),
                    readOnly: true,
                  );
                }),
            ],
          ),
        );
      },
    );
  }
}

class SecurityStudentWarningSummary extends StatelessWidget {
  const SecurityStudentWarningSummary({super.key});

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
      stream: FirebaseFirestore.instance.collection('violations').snapshots(),
      builder: (context, snapshot) {
        if (snapshot.hasError) return ErrorView(message: snapshot.error.toString());
        if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());

        final studentRows = <String, Map<String, dynamic>>{};
        for (final student in sampleStudents) {
          final id = student['id'].toString();
          studentRows[id] = {
            'id': id,
            'name': student['name']?.toString() ?? 'Student $id',
            'major': student['major']?.toString() ?? '',
            'warnings': 0,
          };
        }

        for (final doc in confirmedViolationDocs(snapshot.data!)) {
          final data = doc.data();
          final id = (data['studentId'] ?? '').toString();
          if (id.isEmpty) continue;
          studentRows.putIfAbsent(id, () => {
            'id': id,
            'name': data['studentName']?.toString() ?? 'Student $id',
            'major': data['studentMajor']?.toString() ?? '',
            'warnings': 0,
          });
          studentRows[id]!['warnings'] = (studentRows[id]!['warnings'] as int) + 1;
          if ((studentRows[id]!['name'] ?? '').toString().startsWith('Student ')) {
            studentRows[id]!['name'] = data['studentName']?.toString() ?? studentRows[id]!['name'];
          }
        }

        final rows = studentRows.values.toList()
          ..sort((a, b) {
            final warningCompare = (b['warnings'] as int).compareTo(a['warnings'] as int);
            if (warningCompare != 0) return warningCompare;
            return a['name'].toString().compareTo(b['name'].toString());
          });

        final totalWarnings = rows.fold<int>(0, (sum, row) => sum + (row['warnings'] as int));
        final studentsWithWarnings = rows.where((row) => (row['warnings'] as int) > 0).length;

        return AppCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Student Warning Summary', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 18)),
              const SizedBox(height: 8),
              const Text(
                'Security guard can monitor each student warning count and fine amount. Fine policy: 1000 EGP for every 3 warnings.',
                style: TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(child: StatCard(title: 'Total', value: totalWarnings.toString(), color: nguMaroon, icon: Icons.warning_amber_rounded)),
                  const SizedBox(width: 10),
                  Expanded(child: StatCard(title: 'Students', value: studentsWithWarnings.toString(), color: nguGold, icon: Icons.groups_2_outlined)),
                ],
              ),
              const SizedBox(height: 12),
              ...rows.map((row) {
                final warningCount = row['warnings'] as int;
                final fineAmount = calculateFineAmount(warningCount);
                return Container(
                  margin: const EdgeInsets.only(bottom: 10),
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: warningCount > 0 ? const Color(0xFFFFF4F4) : const Color(0xFFF6F7FA),
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: warningCount > 0 ? Colors.red.withOpacity(0.25) : Colors.black.withOpacity(0.06)),
                  ),
                  child: Row(
                    children: [
                      CircleAvatar(
                        backgroundColor: warningCount > 0 ? nguMaroon : Colors.grey.shade400,
                        child: Text(row['name'].toString().isNotEmpty ? row['name'].toString()[0].toUpperCase() : '?', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(row['name'].toString(), style: const TextStyle(fontWeight: FontWeight.w900)),
                            const SizedBox(height: 3),
                            Text('${row['id']} • ${row['major']}', style: const TextStyle(color: Colors.grey)),
                            const SizedBox(height: 3),
                            Text('Fine: ${formatMoneyEgp(fineAmount)}', style: TextStyle(color: fineAmount > 0 ? Colors.red : Colors.grey, fontWeight: FontWeight.bold)),
                          ],
                        ),
                      ),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          Text(warningCount.toString(), style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: nguMaroon)),
                          const Text('warnings', style: TextStyle(color: Colors.grey)),
                        ],
                      ),
                    ],
                  ),
                );
              }),
            ],
          ),
        );
      },
    );
  }
}

// STUDENT WARNINGS

class StudentWarningsPage extends StatelessWidget {
  final String studentId;
  final String studentName;

  const StudentWarningsPage({
    super.key,
    required this.studentId,
    required this.studentName,
  });

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
      stream: FirebaseFirestore.instance
          .collection('violations')
          .where('studentId', isEqualTo: studentId)
          .snapshots(),
      builder: (context, snapshot) {
        if (snapshot.hasError) return ErrorView(message: snapshot.error.toString());
        if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());

        final docs = confirmedViolationDocs(snapshot.data!);
        final warningCount = docs.length;
        final fineAmount = calculateFineAmount(warningCount);
        final warningsUntilNextFine = 3 - (warningCount % 3 == 0 ? 0 : warningCount % 3);

        return SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              HeaderCard(
                title: 'Welcome, $studentName',
                subtitle: 'Only confirmed violations assigned to your student ID appear here.',
                icon: Icons.school,
              ),
              const SizedBox(height: 16),
              AppCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Student Profile', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 18)),
                    const SizedBox(height: 8),
                    InfoLine(label: 'Name', value: studentName),
                    InfoLine(label: 'Student ID', value: studentId),
                  ],
                ),
              ),
              Row(
                children: [
                  Expanded(child: StatCard(title: 'Warnings', value: warningCount.toString(), color: nguMaroon, icon: Icons.warning_amber_rounded)),
                  const SizedBox(width: 10),
                  Expanded(child: StatCard(title: 'Fine', value: formatMoneyEgp(fineAmount), color: Colors.red, icon: Icons.payments_outlined)),
                ],
              ),
              const SizedBox(height: 10),
              AppCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Fine Policy', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 18)),
                    const SizedBox(height: 8),
                    const Text('A fine of 1000 EGP is applied for every 3 confirmed warnings.'),
                    const SizedBox(height: 8),
                    InfoLine(label: 'Total confirmed warnings', value: warningCount.toString()),
                    InfoLine(label: 'Total fine amount', value: formatMoneyEgp(fineAmount)),
                    if (warningCount % 3 == 0 && warningCount > 0)
                      const Text('A fine has been applied for the latest group of 3 warnings.', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold))
                    else
                      Text('$warningsUntilNextFine more warning(s) until the next 1000 EGP fine.', style: const TextStyle(color: Colors.grey)),
                  ],
                ),
              ),
              SectionTitle(title: 'Confirmed Warnings', trailing: '$warningCount total'),
              if (docs.isEmpty)
                const EmptyCard(text: 'No confirmed violations found for your student ID.')
              else
                ...docs.map((doc) {
                  final data = doc.data();
                  return AppCard(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            const Icon(Icons.warning_amber_rounded, color: nguMaroon),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                'Warning: ${data['violationType'] ?? 'Violation'}',
                                style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 18),
                              ),
                            ),
                            StatusBadge(status: data['status'] ?? 'New'),
                          ],
                        ),
                        const SizedBox(height: 10),
                        DetectionPhoto(data: data),
                        const SizedBox(height: 8),
                        InfoLine(label: 'Location', value: data['location'] ?? '-'),
                        InfoLine(label: 'Status', value: data['status'] ?? 'New'),
                        InfoLine(label: 'Robot', value: data['robotId'] ?? '-'),
                        InfoLine(label: 'Confidence', value: formatConfidence(data['confidence'])),
                        const SizedBox(height: 12),
                        const Text(
                          'This warning was assigned only after security guard review and confirmation.',
                          style: TextStyle(color: Colors.grey),
                        ),
                      ],
                    ),
                  );
                }),
            ],
          ),
        );
      },
    );
  }
}

// PROFESSOR LOOKUP

class ProfessorLookupPage extends StatefulWidget {
  const ProfessorLookupPage({super.key});

  @override
  State<ProfessorLookupPage> createState() => _ProfessorLookupPageState();
}

class _ProfessorLookupPageState extends State<ProfessorLookupPage> {
  String selectedDay = 'Sunday';
  String selectedTimeSlot = '09:00';
  String? selectedProfessorId;
  List<Map<String, dynamic>> professorOptions = [];
  Map<String, dynamic>? resultProfessor;
  Map<String, dynamic>? resultSlot;
  String? error;
  String? resultNote;
  bool loading = false;
  bool loadingProfessors = true;

  final days = const ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'];
  final timeSlots = const [
    '09:00',
    '10:00',
    '11:00',
    '12:00',
    '13:00',
    '14:00',
    '15:00',
    '16:00',
  ];

  @override
  void initState() {
    super.initState();
    loadProfessors();
  }

  Future<void> loadProfessors({bool seedIfEmpty = true}) async {
    setState(() => loadingProfessors = true);

    var snapshot = await FirebaseFirestore.instance.collection('professors').orderBy('name').get();

    if (snapshot.docs.isEmpty && seedIfEmpty) {
      await seedSampleProfessors();
      snapshot = await FirebaseFirestore.instance.collection('professors').orderBy('name').get();
    }

    final sampleProfessorIds = sampleProfessors.map((p) => p['id'].toString()).toSet();
    final loadedByName = <String, Map<String, dynamic>>{};

    for (final doc in snapshot.docs) {
      final data = doc.data();
      final name = (data['name'] ?? doc.id).toString().trim();
      final key = name.toLowerCase();
      final professor = {
        ...data,
        'id': doc.id,
      };

      // If older duplicated demo documents exist in Firestore, show the professor once.
      // Prefer the clean sample document IDs when they are present.
      if (!loadedByName.containsKey(key) || sampleProfessorIds.contains(doc.id)) {
        loadedByName[key] = professor;
      }
    }

    final loaded = loadedByName.values.toList()
      ..sort((a, b) => (a['name'] ?? '').toString().compareTo((b['name'] ?? '').toString()));

    setState(() {
      professorOptions = loaded;
      if (loaded.isEmpty) {
        selectedProfessorId = null;
      } else if (selectedProfessorId == null || !loaded.any((prof) => prof['id'].toString() == selectedProfessorId)) {
        selectedProfessorId = loaded.first['id'].toString();
      }
      loadingProfessors = false;
    });
  }

  Future<void> seedProfessorsFromPage() async {
    await seedSampleProfessors();
    await loadProfessors(seedIfEmpty: false);
    if (mounted) showSnack(context, 'Sample professor schedules added to Firebase');
  }

  Future<void> searchProfessorSchedule() async {
    if (selectedProfessorId == null || selectedProfessorId!.isEmpty) {
      setState(() {
        error = 'Choose a professor first. If the list is empty, add sample professor schedules.';
        resultProfessor = null;
        resultSlot = null;
        resultNote = null;
      });
      return;
    }

    setState(() => loading = true);

    final doc = await FirebaseFirestore.instance.collection('professors').doc(selectedProfessorId).get();

    if (!doc.exists) {
      setState(() {
        loading = false;
        error = 'Professor not found. Add sample professor schedules first.';
        resultProfessor = null;
        resultSlot = null;
        resultNote = null;
      });
      return;
    }

    final foundProfessor = {
      ...doc.data()!,
      'id': doc.id,
    };

    Map<String, dynamic>? foundSlot;
    final rawSchedule = foundProfessor['schedule'];
    if (rawSchedule is List) {
      for (final entry in rawSchedule) {
        if (entry is Map) {
          final slot = Map<String, dynamic>.from(entry);
          final day = (slot['day'] ?? '').toString();
          final start = (slot['start'] ?? '').toString();
          final end = (slot['end'] ?? '').toString();
          if (day == selectedDay && isTimeInsideSlot(selectedTimeSlot, start, end)) {
            foundSlot = slot;
            break;
          }
        }
      }
    }

    setState(() {
      loading = false;
      resultProfessor = foundProfessor;
      resultSlot = foundSlot;
      error = null;
      if (foundSlot == null) {
        resultNote = 'No lecture or scheduled activity at $selectedTimeSlot on $selectedDay. Location shown as the professor office.';
      } else {
        resultNote = 'Lecture/activity room found for $selectedDay at $selectedTimeSlot.';
      }
    });
  }

  List<Map<String, dynamic>> professorSchedule(Map<String, dynamic> professor) {
    final rawSchedule = professor['schedule'];
    if (rawSchedule is! List) return [];
    return rawSchedule.whereType<Map>().map((item) => Map<String, dynamic>.from(item)).toList();
  }

  @override
  Widget build(BuildContext context) {
    final professor = resultProfessor;
    final schedule = professor == null ? <Map<String, dynamic>>[] : professorSchedule(professor);

    return PageContainer(
      children: [
        const HeaderCard(
          title: 'Professor Lookup',
          subtitle: 'Choose professor, day, and time slot. If the professor has a lecture, the app shows the lecture room. Otherwise, it shows the professor office.',
          icon: Icons.person_search,
        ),
        const SizedBox(height: 16),
        AppCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Professor Name', style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              if (loadingProfessors)
                const Center(child: CircularProgressIndicator())
              else
                DropdownButtonFormField<String>(
                  value: selectedProfessorId,
                  decoration: inputDecoration('Choose professor'),
                  items: professorOptions.map((prof) {
                    return DropdownMenuItem<String>(
                      value: prof['id'].toString(),
                      child: Text(prof['name']?.toString() ?? prof['id'].toString()),
                    );
                  }).toList(),
                  onChanged: (value) {
                    if (value != null) {
                      setState(() {
                        selectedProfessorId = value;
                        resultProfessor = null;
                        resultSlot = null;
                        resultNote = null;
                        error = null;
                      });
                    }
                  },
                ),
              const SizedBox(height: 12),
              const Text('Day', style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              DropdownButtonFormField<String>(
                value: selectedDay,
                decoration: inputDecoration('Choose day'),
                items: days.map((day) => DropdownMenuItem(value: day, child: Text(day))).toList(),
                onChanged: (value) {
                  if (value != null) {
                    setState(() {
                      selectedDay = value;
                      resultProfessor = null;
                      resultSlot = null;
                      resultNote = null;
                      error = null;
                    });
                  }
                },
              ),
              const SizedBox(height: 12),
              const Text('Time Slot', style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              DropdownButtonFormField<String>(
                value: selectedTimeSlot,
                decoration: inputDecoration('Choose time slot'),
                items: timeSlots.map((time) => DropdownMenuItem(value: time, child: Text(time))).toList(),
                onChanged: (value) {
                  if (value != null) {
                    setState(() {
                      selectedTimeSlot = value;
                      resultProfessor = null;
                      resultSlot = null;
                      resultNote = null;
                      error = null;
                    });
                  }
                },
              ),
              const SizedBox(height: 14),
              PrimaryButton(text: loading ? 'Searching...' : 'Search Schedule', onPressed: loading || loadingProfessors ? () {} : searchProfessorSchedule),
              TextButton(onPressed: seedProfessorsFromPage, child: const Text('Refresh / Add sample professor schedules')),
            ],
          ),
        ),
        if (error != null) ErrorBox(text: error!),
        if (resultNote != null)
          AppCard(
            child: Text(
              resultNote!,
              style: TextStyle(color: resultSlot == null ? nguGold : Colors.green, fontWeight: FontWeight.w900),
            ),
          ),
        if (professor != null)
          AppCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(professor['name'] ?? '-', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900)),
                const SizedBox(height: 10),
                InfoLine(label: 'Department', value: professor['department'] ?? '-'),
                InfoLine(label: 'Office', value: professor['office'] ?? '-'),
                InfoLine(label: 'Email', value: professor['email'] ?? '-'),
                const Divider(height: 24),
                const Text('Location at selected time', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 18)),
                const SizedBox(height: 8),
                InfoLine(label: 'Day', value: selectedDay),
                InfoLine(label: 'Time Slot', value: selectedTimeSlot),
                if (resultSlot != null) ...[
                  InfoLine(label: 'Room / Location', value: resultSlot!['location'] ?? '-'),
                  InfoLine(label: 'Activity', value: resultSlot!['activity'] ?? '-'),
                  InfoLine(label: 'Course', value: resultSlot!['course'] ?? '-'),
                  InfoLine(label: 'Scheduled Time', value: '${resultSlot!['start'] ?? '-'} - ${resultSlot!['end'] ?? '-'}'),
                ] else ...[
                  InfoLine(label: 'Room / Location', value: professor['office'] ?? '-'),
                  const SizedBox(height: 6),
                  const Text('Reason: no lecture/activity is scheduled at this time slot.', style: TextStyle(color: Colors.grey)),
                ],
              ],
            ),
          ),
        if (schedule.isNotEmpty) ...[
          SectionTitle(title: 'Full Weekly Schedule', trailing: '${schedule.length} scheduled activities'),
          ...schedule.map((slot) {
            return AppCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('${slot['day'] ?? '-'} • ${slot['start'] ?? '-'} - ${slot['end'] ?? '-'}', style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 16)),
                  const SizedBox(height: 6),
                  InfoLine(label: 'Room / Location', value: slot['location'] ?? '-'),
                  InfoLine(label: 'Activity', value: slot['activity'] ?? '-'),
                  InfoLine(label: 'Course', value: slot['course'] ?? '-'),
                ],
              ),
            );
          }),
        ],
      ],
    );
  }
}

// ROBOT SIMULATOR - SECURITY ONLY

class RobotSimulatorPage extends StatefulWidget {
  const RobotSimulatorPage({super.key});

  @override
  State<RobotSimulatorPage> createState() => _RobotSimulatorPageState();
}

class _RobotSimulatorPageState extends State<RobotSimulatorPage> {
  final typeController = TextEditingController(text: 'Smoking');
  final locationController = TextEditingController(text: 'Building A - Floor 2');
  final robotController = TextEditingController(text: 'TB4-01');
  final confidenceController = TextEditingController(text: '0.82');
  final photoUrlController = TextEditingController();

  @override
  void dispose() {
    typeController.dispose();
    locationController.dispose();
    robotController.dispose();
    confidenceController.dispose();
    photoUrlController.dispose();
    super.dispose();
  }

  Future<void> sendDetection() async {
    await FirebaseFirestore.instance.collection('smoke_detections').add({
      'detectionType': typeController.text.trim().isEmpty ? 'Smoking' : typeController.text.trim(),
      'location': locationController.text.trim(),
      'robotId': robotController.text.trim(),
      'confidence': double.tryParse(confidenceController.text.trim()) ?? 0.0,
      'photoUrl': photoUrlController.text.trim(),
      'status': 'Pending Review',
      'source': 'Robot Simulator',
      'timestamp': FieldValue.serverTimestamp(),
    });
    if (mounted) showSnack(context, 'Pending smoke detection sent for security review');
  }

  Future<void> addSampleDatabase() async {
    await seedSampleDatabase();
    if (mounted) showSnack(context, 'Sample students and professor schedules were added to Firebase');
  }

  @override
  Widget build(BuildContext context) {
    return PageContainer(
      children: [
        const HeaderCard(
          title: 'Robot Detection Simulator',
          subtitle: 'Creates pending smoke detections. It does not create student violations automatically.',
          icon: Icons.smart_toy,
        ),
        const SizedBox(height: 16),
        AppCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Sample Database', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 18)),
              const SizedBox(height: 8),
              const Text(
                'Add sample students and full professor schedules to Firestore. Use these student IDs when confirming a true violation.',
                style: TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 12),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: sampleStudents.map((student) {
                  return Chip(label: Text('${student['id']} • ${student['name']}'));
                }).toList(),
              ),
              const SizedBox(height: 14),
              PrimaryButton(text: 'Add Sample Students + Professors', onPressed: addSampleDatabase),
            ],
          ),
        ),
        AppCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Simulate Robot Detection',
                style: TextStyle(fontWeight: FontWeight.w900, fontSize: 18),
              ),
              const SizedBox(height: 10),
              TextField(controller: typeController, decoration: inputDecoration('Detection Type')),
              const SizedBox(height: 10),
              TextField(controller: locationController, decoration: inputDecoration('Location')),
              const SizedBox(height: 10),
              TextField(controller: robotController, decoration: inputDecoration('Robot ID')),
              const SizedBox(height: 10),
              TextField(
                controller: confidenceController,
                keyboardType: TextInputType.number,
                decoration: inputDecoration('Confidence'),
              ),
              const SizedBox(height: 10),
              TextField(
                controller: photoUrlController,
                decoration: inputDecoration('Optional Photo URL'),
              ),
              const SizedBox(height: 14),
              PrimaryButton(text: 'Send Pending Detection', onPressed: sendDetection),
            ],
          ),
        ),
      ],
    );
  }
}

// SHARED COMPONENTS

String formatConfidence(dynamic confidence) {
  if (confidence == null) return 'N/A';
  final value = confidence is num ? confidence.toDouble() : double.tryParse(confidence.toString());
  if (value == null) return 'N/A';
  return '${(value * 100).round()}%';
}

int calculateFineAmount(int warningCount) {
  return (warningCount ~/ 3) * 1000;
}

String formatMoneyEgp(int amount) {
  return '$amount EGP';
}

List<QueryDocumentSnapshot<Map<String, dynamic>>> confirmedViolationDocs(
  QuerySnapshot<Map<String, dynamic>> snapshot,
) {
  return snapshot.docs.where((doc) => doc.data()['confirmed'] == true).toList();
}

class DetectionPhoto extends StatelessWidget {
  final Map<String, dynamic> data;

  const DetectionPhoto({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    final photoUrl = (data['photoUrl'] ?? data['imageUrl'] ?? '').toString();
    final photoBase64 = (data['photoBase64'] ?? '').toString();

    Widget child;

    if (photoBase64.isNotEmpty) {
      try {
        child = Image.memory(base64Decode(photoBase64), width: double.infinity, height: 180, fit: BoxFit.cover);
      } catch (_) {
        child = const Center(child: Text('Invalid photo data', style: TextStyle(color: Colors.grey)));
      }
    } else if (photoUrl.isNotEmpty) {
      child = Image.network(
        photoUrl,
        width: double.infinity,
        height: 180,
        fit: BoxFit.cover,
        errorBuilder: (_, __, ___) => const Center(
          child: Text('Photo could not be loaded', style: TextStyle(color: Colors.grey)),
        ),
      );
    } else {
      child = const Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.image_not_supported_outlined, color: Colors.grey, size: 34),
            SizedBox(height: 6),
            Text('No detection photo attached', style: TextStyle(color: Colors.grey)),
          ],
        ),
      );
    }

    return ClipRRect(
      borderRadius: BorderRadius.circular(14),
      child: Container(
        width: double.infinity,
        height: 180,
        color: const Color(0xFFF0F2F6),
        child: child,
      ),
    );
  }
}

class SmokeDetectionCard extends StatelessWidget {
  final String id;
  final Map<String, dynamic> data;
  final VoidCallback? onFalseAlarm;
  final VoidCallback? onConfirmViolation;
  final bool readOnly;

  const SmokeDetectionCard({
    super.key,
    required this.id,
    required this.data,
    this.onFalseAlarm,
    this.onConfirmViolation,
    this.readOnly = false,
  });

  @override
  Widget build(BuildContext context) {
    final detectionType = data['detectionType'] ?? 'Smoking';
    final location = data['location'] ?? '-';
    final robotId = data['robotId'] ?? '-';
    final status = data['status'] ?? 'Pending Review';
    final source = data['source'] ?? 'Robot ML Detection';
    final assignedStudentId = (data['assignedStudentId'] ?? '').toString();
    final assignedStudentName = (data['assignedStudentName'] ?? '').toString();

    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const CircleAvatar(
                backgroundColor: nguMaroon,
                child: Icon(Icons.smoking_rooms, color: Colors.white),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  '$detectionType Detection',
                  style: const TextStyle(fontSize: 19, fontWeight: FontWeight.w900),
                ),
              ),
              StatusBadge(status: status),
            ],
          ),
          const SizedBox(height: 14),
          DetectionPhoto(data: data),
          const SizedBox(height: 12),
          InfoLine(label: 'Location', value: location.toString()),
          InfoLine(label: 'Robot', value: robotId.toString()),
          InfoLine(label: 'Confidence', value: formatConfidence(data['confidence'])),
          InfoLine(label: 'Source', value: source.toString()),
          if (assignedStudentId.isNotEmpty) InfoLine(label: 'Assigned Student ID', value: assignedStudentId),
          if (assignedStudentName.isNotEmpty) InfoLine(label: 'Assigned Student Name', value: assignedStudentName),
          if (!readOnly) ...[
            const SizedBox(height: 12),
            const Text(
              'Review the photo. Confirm only if this is a true smoking violation, then enter the student ID manually.',
              style: TextStyle(color: Colors.grey),
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                SmallButton(text: 'False Alarm', color: Colors.purple, onPressed: onFalseAlarm ?? () {}),
                SmallButton(text: 'True Violation', color: Colors.green, onPressed: onConfirmViolation ?? () {}),
              ],
            ),
          ],
        ],
      ),
    );
  }
}

class ViolationCard extends StatelessWidget {
  final String id;
  final Map<String, dynamic> data;
  final VoidCallback onSeen;
  final VoidCallback onResolved;
  final VoidCallback onFalseAlarm;

  const ViolationCard({
    super.key,
    required this.id,
    required this.data,
    required this.onSeen,
    required this.onResolved,
    required this.onFalseAlarm,
  });

  @override
  Widget build(BuildContext context) {
    final violationType = data['violationType'] ?? 'Violation';
    final studentName = data['studentName'] ?? 'Unknown Student';
    final studentId = data['studentId'] ?? 'Unknown';
    final location = data['location'] ?? '-';
    final robotId = data['robotId'] ?? '-';
    final status = data['status'] ?? 'New';
    final confidence = data['confidence'];

    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              CircleAvatar(
                backgroundColor: nguMaroon,
                child: Text(
                  studentName.toString().isNotEmpty ? studentName.toString()[0].toUpperCase() : '?',
                  style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  violationType,
                  style: const TextStyle(fontSize: 19, fontWeight: FontWeight.w900),
                ),
              ),
              StatusBadge(status: status),
            ],
          ),
          const SizedBox(height: 14),
          InfoLine(label: 'Student', value: '$studentName ($studentId)'),
          InfoLine(label: 'Location', value: location),
          InfoLine(label: 'Robot', value: robotId),
          InfoLine(label: 'Confidence', value: confidence == null ? 'N/A' : '${(confidence * 100).round()}%'),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              SmallButton(text: 'Seen', color: Colors.grey, onPressed: onSeen),
              SmallButton(text: 'Resolve', color: Colors.green, onPressed: onResolved),
              SmallButton(text: 'False Alarm', color: Colors.red, onPressed: onFalseAlarm),
            ],
          ),
        ],
      ),
    );
  }
}

class HeaderCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final IconData icon;

  const HeaderCard({
    super.key,
    required this.title,
    required this.subtitle,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [nguMaroon, nguDarkMaroon],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(22),
        boxShadow: [
          BoxShadow(
            color: nguMaroon.withOpacity(0.22),
            blurRadius: 18,
            offset: const Offset(0, 8),
          )
        ],
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 28,
            backgroundColor: Colors.white.withOpacity(0.16),
            child: Icon(icon, color: Colors.white, size: 30),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('NEWGIZA University', style: TextStyle(color: Colors.white70)),
                const SizedBox(height: 4),
                Text(
                  title,
                  style: const TextStyle(color: Colors.white, fontSize: 23, fontWeight: FontWeight.w900),
                ),
                const SizedBox(height: 4),
                Text(subtitle, style: const TextStyle(color: Colors.white70)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class AppCard extends StatelessWidget {
  final Widget child;

  const AppCard({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(bottom: 14),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: const Color(0xFFECEEF3)),
        borderRadius: BorderRadius.circular(18),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.045),
            blurRadius: 15,
            offset: const Offset(0, 8),
          )
        ],
      ),
      child: child,
    );
  }
}

class StatCard extends StatelessWidget {
  final String title;
  final String value;
  final Color color;
  final IconData icon;

  const StatCard({
    super.key,
    required this.title,
    required this.value,
    required this.color,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 28),
          const SizedBox(height: 10),
          Text(value, style: TextStyle(color: color, fontWeight: FontWeight.w900, fontSize: 26)),
          Text(title, style: const TextStyle(color: Colors.grey, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}

class SectionTitle extends StatelessWidget {
  final String title;
  final String? trailing;

  const SectionTitle({super.key, required this.title, this.trailing});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 6, bottom: 10),
      child: Row(
        children: [
          Expanded(child: Text(title, style: const TextStyle(fontSize: 19, fontWeight: FontWeight.w900))),
          if (trailing != null)
            Text(trailing!, style: const TextStyle(color: nguMaroon, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}

class InfoLine extends StatelessWidget {
  final String label;
  final String value;

  const InfoLine({super.key, required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 7),
      child: RichText(
        text: TextSpan(
          style: const TextStyle(color: Colors.black87, fontSize: 14),
          children: [
            TextSpan(text: '$label: ', style: const TextStyle(fontWeight: FontWeight.w900)),
            TextSpan(text: value, style: const TextStyle(color: Colors.grey)),
          ],
        ),
      ),
    );
  }
}

class StatusBadge extends StatelessWidget {
  final String status;

  const StatusBadge({super.key, required this.status});

  @override
  Widget build(BuildContext context) {
    Color bg;
    Color fg;

    if (status == 'Resolved' || status == 'Completed') {
      bg = Colors.green.withOpacity(0.12);
      fg = Colors.green;
    } else if (status == 'Seen' || status == 'In Progress') {
      bg = nguGold.withOpacity(0.16);
      fg = nguGold;
    } else if (status == 'False Alarm' || status == 'Cancelled') {
      bg = Colors.purple.withOpacity(0.12);
      fg = Colors.purple;
    } else {
      bg = nguMaroon.withOpacity(0.12);
      fg = nguMaroon;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 6),
      decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(50)),
      child: Text(status, style: TextStyle(color: fg, fontWeight: FontWeight.w900, fontSize: 12)),
    );
  }
}

class PrimaryButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;

  const PrimaryButton({super.key, required this.text, required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: 52,
      child: ElevatedButton(
        onPressed: onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: nguMaroon,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        ),
        child: Text(text, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w900)),
      ),
    );
  }
}

class SmallButton extends StatelessWidget {
  final String text;
  final Color color;
  final VoidCallback onPressed;

  const SmallButton({
    super.key,
    required this.text,
    required this.color,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        foregroundColor: Colors.white,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
      child: Text(text, style: const TextStyle(fontWeight: FontWeight.bold)),
    );
  }
}

class EmptyCard extends StatelessWidget {
  final String text;

  const EmptyCard({super.key, required this.text});

  @override
  Widget build(BuildContext context) {
    return AppCard(
      child: Text(text, textAlign: TextAlign.center, style: const TextStyle(color: Colors.grey)),
    );
  }
}

class ErrorView extends StatelessWidget {
  final String message;

  const ErrorView({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Text(message, textAlign: TextAlign.center, style: const TextStyle(color: Colors.red)),
      ),
    );
  }
}

class ErrorBox extends StatelessWidget {
  final String text;

  const ErrorBox({super.key, required this.text});

  @override
  Widget build(BuildContext context) {
    return AppCard(
      child: Text(text, style: const TextStyle(color: Colors.red, fontWeight: FontWeight.bold)),
    );
  }
}

class PageContainer extends StatelessWidget {
  final List<Widget> children;

  const PageContainer({super.key, required this.children});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(children: children),
    );
  }
}

InputDecoration inputDecoration(String hint) {
  return InputDecoration(
    hintText: hint,
    filled: true,
    fillColor: Colors.white,
    border: OutlineInputBorder(borderRadius: BorderRadius.circular(14)),
    enabledBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(14),
      borderSide: const BorderSide(color: Color(0xFFD8DCE5)),
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(14),
      borderSide: const BorderSide(color: nguMaroon, width: 2),
    ),
  );
}

void showSnack(BuildContext context, String message) {
  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
}