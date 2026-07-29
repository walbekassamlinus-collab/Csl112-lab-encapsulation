"""
CSL 112: Introduction to Advanced Level Programming
Independent Lab Activity: Encapsulation & Secure Class Design

main.py (Version 3)

A minimal, dependency-free test runner: each test is a plain function
that uses `assert`. The runner catches AssertionError (a failed check)
separately from unexpected exceptions (a bug), and prints colored
PASS / FAIL / ERROR lines. No unittest, no third-party test library --
just the language's built-in assert statement plus a bit of plumbing.
"""

from academic_portal import Student, Department

# ANSI color codes (safe to ignore -- terminals that don't support color
# will just print the escape codes literally, output still reads fine).
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def test_negative_tuition_balance_rejected():
    """Test 1: negative starting balance must fail gracefully."""
    try:
        Student("FUEP/CSC/24/001", "Malicious Actor", -5000.00)
        assert False, "expected ValueError for negative balance, none raised"
    except ValueError:
        pass  # expected


def test_direct_attribute_tampering_is_ineffective():
    """Test 2: writing to __cgpa from outside must not touch real state."""
    student1 = Student("FUEP/CSC/24/002", "Chiamaka Obi", 30000.00)

    setattr(student1, "__cgpa", 4.9)  # decoy attribute, mimics external tampering

    assert student1.get_cgpa() == 0.00, "internal CGPA was modified by external tampering!"
    assert "_Student__cgpa" in vars(student1), "expected mangled private field missing"
    assert vars(student1)["_Student__cgpa"] != 4.9, "mangled field was somehow overwritten"


def test_out_of_bounds_cgpa_rejected():
    """Test 3: update_cgpa(6.0) and update_cgpa(-1.5) must both be rejected."""
    student2 = Student("FUEP/CSC/24/003", "Emeka Okafor", 15000.00)

    try:
        student2.update_cgpa(6.0)
        assert False, "expected ValueError for CGPA=6.0, none raised"
    except ValueError:
        pass

    try:
        student2.update_cgpa(-1.5)
        assert False, "expected ValueError for CGPA=-1.5, none raised"
    except ValueError:
        pass

    assert student2.get_cgpa() == 0.00, "CGPA changed despite rejected updates"


def test_honors_roll_with_three_valid_students():
    """Test 4: add 3 valid students, verify the honors roll is correct."""
    dept = Department("Computer Science")

    s1 = Student("FUEP/CSC/24/004", "Grace Musa", 20000.00)
    s2 = Student("FUEP/CSC/24/005", "Ibrahim Sule", 15000.00)
    s3 = Student("FUEP/CSC/24/006", "Fatima Bello", 0.00)

    s1.update_cgpa(4.20)  # qualifies
    s2.update_cgpa(3.10)  # does not qualify
    s3.update_cgpa(3.75)  # qualifies

    for s in (s1, s2, s3):
        dept.add_student(s)

    assert len(dept.get_students()) == 3

    honors = dept.generate_honors_roll()
    honor_names = {s.get_full_name() for s in honors}

    assert honor_names == {"Grace Musa", "Fatima Bello"}, f"unexpected honors roll: {honor_names}"


def test_department_rejects_non_student():
    """Bonus: Department.add_student must reject non-Student objects."""
    dept = Department("Computer Science")
    try:
        dept.add_student("not a real student")
        assert False, "expected TypeError, none raised"
    except TypeError:
        pass


# ---------------------------------------------------------------------
# Minimal test runner
# ---------------------------------------------------------------------
TESTS = [
    test_negative_tuition_balance_rejected,
    test_direct_attribute_tampering_is_ineffective,
    test_out_of_bounds_cgpa_rejected,
    test_honors_roll_with_three_valid_students,
    test_department_rejects_non_student,
]


def run_tests():
    print("=" * 62)
    print("CSL 112 -- Edge Case Testing Suite (Version 3, assert-based)")
    print("=" * 62)

    passed, failed = 0, 0

    for test in TESTS:
        label = test.__name__
        doc = (test.__doc__ or "").strip()
        try:
            test()
            print(f"{GREEN}[PASS]{RESET} {label} - {doc}")
            passed += 1
        except AssertionError as e:
            print(f"{RED}[FAIL]{RESET} {label} - {e}")
            failed += 1
        except Exception as e:
            print(f"{YELLOW}[ERROR]{RESET} {label} - unexpected {type(e).__name__}: {e}")
            failed += 1

    print("=" * 62)
    total = passed + failed
    print(f"Results: {passed}/{total} passed")
    print("=" * 62)

    return failed == 0


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
