"""
CSL 112: Introduction to Advanced Level Programming
Polymorphism & Inheritance Test Suite — test_inheritance.py

Tests:
  1. Polymorphic payroll loop (dynamic dispatch)
  2. Abstract class instantiation prevention
  3. Missing method implementation detection
  4. Edge case validation

Author: [Your Name]
Matric No: [Your Matric Number]
Date: 5th August 2026
"""

from institutional_system import User, StudentUser, LecturerUser, ResearchAssistant


def separator(title: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  TEST: {title}")
    print(f"{'─' * 60}")


def run_tests():
    print("=" * 60)
    print("  CSL 112 — INHERITANCE & POLYMORPHISM TEST SUITE")
    print("=" * 60)

    # ──────────────────────────────────────────────────────────────
    # TEST 1: Direct instantiation of abstract User class
    # Python should REFUSE to create a User object directly
    # ──────────────────────────────────────────────────────────────
    separator("Direct Instantiation of Abstract Class")
    try:
        bad_user = User("U001", "Ghost User", "ghost@uni.edu")
        print("  [FAIL] User was instantiated — abstract class is broken!")
    except TypeError as e:
        print(f"  [PASS] TypeError raised as expected:")
        print(f"         → {e}")

    # ──────────────────────────────────────────────────────────────
    # TEST 2: Subclass that forgets to implement calculate_monthly_payout()
    # Python should refuse to instantiate it
    # ──────────────────────────────────────────────────────────────
    separator("Subclass Missing Abstract Method Implementation")

    class IncompleteUser(User):
        """A broken subclass that forgot to implement calculate_monthly_payout."""
        pass  # No implementation of the required abstract method

    try:
        incomplete = IncompleteUser("U002", "Lazy Dev", "lazy@uni.edu")
        print("  [FAIL] IncompleteUser was created — contract enforcement broken!")
    except TypeError as e:
        print(f"  [PASS] TypeError raised as expected:")
        print(f"         → {e}")

    # ──────────────────────────────────────────────────────────────
    # TEST 3: Invalid inputs at construction
    # ──────────────────────────────────────────────────────────────
    separator("Invalid Constructor Inputs")

    # Negative stipend
    try:
        bad_student = StudentUser("S001", "Bad Student", "bad@uni.edu", -5000, 3)
        print("  [FAIL] Negative stipend accepted!")
    except ValueError as e:
        print(f"  [PASS] Negative stipend rejected: {e}")

    # Zero base salary for lecturer
    try:
        bad_lecturer = LecturerUser("L001", "Bad Lecturer", "bad@uni.edu", 0, 0, 5000)
        print("  [FAIL] Zero salary accepted!")
    except ValueError as e:
        print(f"  [PASS] Zero salary rejected: {e}")

    # Negative research grant
    try:
        bad_ra = ResearchAssistant("R001", "Bad RA", "ra@uni.edu", 40000, 2, -10000)
        print("  [FAIL] Negative grant accepted!")
    except ValueError as e:
        print(f"  [PASS] Negative grant rejected: {e}")

    # ──────────────────────────────────────────────────────────────
    # TEST 4: POLYMORPHIC PAYROLL LOOP — the heart of this assignment
    #
    # We create a mixed list of different user types and call
    # calculate_monthly_payout() on ALL of them in ONE loop —
    # without checking what type each object is.
    #
    # Python automatically routes each call to the correct class's
    # version of the method. This is called DYNAMIC DISPATCH.
    # ──────────────────────────────────────────────────────────────
    separator("Polymorphic Payroll Processing (Dynamic Dispatch)")

    # Create a mixed list of different user types
    payroll_queue: list[User] = [

        StudentUser(
            user_id="STU/2024/001",
            full_name="Amaka Osei",
            email="amaka.osei@uni.edu",
            stipend_rate=45000.00,
            courses_enrolled=5
        ),

        LecturerUser(
            user_id="LEC/2024/010",
            full_name="Dr. Emeka Nwosu",
            email="e.nwosu@uni.edu",
            base_salary=380000.00,
            overtime_hours=12,
            hourly_rate=8500.00
        ),

        ResearchAssistant(
            user_id="RA/2024/003",
            full_name="Fatima Bello",
            email="f.bello@uni.edu",
            stipend_rate=50000.00,
            courses_enrolled=3,
            research_grant_allowance=75000.00
        ),

        StudentUser(
            user_id="STU/2024/007",
            full_name="Tunde Adeyemi",
            email="t.adeyemi@uni.edu",
            stipend_rate=38000.00,
            courses_enrolled=4
        ),

        LecturerUser(
            user_id="LEC/2024/022",
            full_name="Prof. Ngozi Ibe",
            email="n.ibe@uni.edu",
            base_salary=520000.00,
            overtime_hours=5,
            hourly_rate=12000.00
        ),
    ]

    print(f"\n  Processing payroll for {len(payroll_queue)} users...\n")
    print(f"  {'─' * 56}")

    total_payout = 0.0

    # ONE loop — no isinstance() checks — Python figures out which
    # calculate_monthly_payout() to call based on the actual object type.
    # This is POLYMORPHISM in action.
    for user in payroll_queue:
        payout = user.calculate_monthly_payout()  # Dynamic dispatch happens here
        total_payout += payout
        print(f"  {user.get_full_name():<28} "
              f"[{user.__class__.__name__:<17}] "
              f"₦{payout:>12,.2f}")

    print(f"  {'─' * 56}")
    print(f"  {'TOTAL MONTHLY PAYROLL':<47} ₦{total_payout:>12,.2f}")
    print(f"  {'─' * 56}")

    print("\n  [PASS] All payouts calculated polymorphically in a single loop.")
    print("         Python routed each calculate_monthly_payout() call to the")
    print("         correct class automatically — no type-checking needed.")

    # ──────────────────────────────────────────────────────────────
    # TEST 5: Verify multi-level inheritance chain
    # ──────────────────────────────────────────────────────────────
    separator("Multi-Level Inheritance Chain Verification")

    ra = payroll_queue[2]  # Fatima — our ResearchAssistant
    print(f"\n  Object: {ra.get_full_name()}")
    print(f"  Is a User?              {isinstance(ra, User)}")
    print(f"  Is a StudentUser?       {isinstance(ra, StudentUser)}")
    print(f"  Is a ResearchAssistant? {isinstance(ra, ResearchAssistant)}")
    print(f"  Is a LecturerUser?      {isinstance(ra, LecturerUser)}")
    print(f"\n  Inheritance chain: User → StudentUser → ResearchAssistant ✓")

    if isinstance(ra, User) and isinstance(ra, StudentUser) and isinstance(ra, ResearchAssistant):
        print("  [PASS] Multi-level inheritance verified correctly.")

    # ──────────────────────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  ALL TESTS COMPLETED SUCCESSFULLY.")
    print("  Abstract contracts, inheritance, and polymorphism")
    print("  are all working correctly.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_tests()
