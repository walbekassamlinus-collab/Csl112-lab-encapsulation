"""
CSL 112: Introduction to Advanced Level Programming
Institutional User & Payroll Management System

Builds upon the Academic Portal (Week 1) by introducing:
  - Abstract Base Classes (ABCs)
  - Inheritance hierarchies
  - Polymorphism & dynamic dispatch

Author: [Your Name]
Matric No: [Your Matric Number]
Date: 5th August 2026
"""

from abc import ABC, abstractmethod


# ══════════════════════════════════════════════════════════════════════════════
# ABSTRACT BASE CLASS: User
# ══════════════════════════════════════════════════════════════════════════════

class User(ABC):
    """
    Abstract Base Class representing any institutional user.

    This class cannot be instantiated directly — it is a blueprint only.
    Any class that inherits from User MUST implement calculate_monthly_payout(),
    otherwise Python will raise a TypeError when you try to create an object.

    Think of it like a contract: every type of user (student, lecturer, etc.)
    must be able to calculate their own monthly payout, but HOW they do it
    differs per role — so each subclass defines its own version.
    """

    def __init__(self, user_id: str, full_name: str, email: str):
        """
        Initialises shared attributes for all institutional users.

        Args:
            user_id (str): Unique identifier for the user.
            full_name (str): User's full name.
            email (str): User's institutional email address.

        Raises:
            ValueError: If any required field is empty.
        """
        if not user_id or not user_id.strip():
            raise ValueError("user_id cannot be empty.")
        if not full_name or not full_name.strip():
            raise ValueError("full_name cannot be empty.")
        if not email or "@" not in email:
            raise ValueError("A valid email address is required.")

        # Protected attributes (single underscore) — accessible to subclasses
        self._user_id: str = user_id.strip()
        self._full_name: str = full_name.strip()
        self._email: str = email.strip()

    # ── Getters ───────────────────────────────────────────────────────────────

    def get_user_id(self) -> str:
        return self._user_id

    def get_full_name(self) -> str:
        return self._full_name

    def get_email(self) -> str:
        return self._email

    # ── Abstract Method (the "contract") ──────────────────────────────────────

    @abstractmethod
    def calculate_monthly_payout(self) -> float:
        """
        Calculates and returns the user's monthly payout.

        This method has NO implementation here — every subclass MUST
        provide its own version or Python will refuse to create objects
        from that subclass.
        """
        pass  # No body — subclasses must define this themselves

    # ── String Representation ─────────────────────────────────────────────────

    def __str__(self) -> str:
        return (
            f"[{self.__class__.__name__}] {self._full_name} "
            f"(ID: {self._user_id} | Email: {self._email})"
        )


# ══════════════════════════════════════════════════════════════════════════════
# DERIVED CLASS 1: StudentUser  (inherits from User)
# ══════════════════════════════════════════════════════════════════════════════

class StudentUser(User):
    """
    Represents a student in the institutional system.

    Inherits all shared attributes from User and adds:
    - A monthly stipend rate
    - Number of courses currently enrolled in

    Monthly payout = stipend_rate minus a fixed 2% student welfare deduction.
    """

    WELFARE_DEDUCTION_RATE = 0.02  # 2% deducted for student welfare dues

    def __init__(self, user_id: str, full_name: str, email: str,
                 stipend_rate: float, courses_enrolled: int):
        """
        Args:
            stipend_rate (float): Monthly stipend amount (must be >= 0).
            courses_enrolled (int): Number of courses (must be >= 1).
        """
        super().__init__(user_id, full_name, email)  # Call User's __init__

        if stipend_rate < 0:
            raise ValueError("Stipend rate cannot be negative.")
        if courses_enrolled < 1:
            raise ValueError("A student must be enrolled in at least 1 course.")

        self.__stipend_rate: float = stipend_rate
        self.__courses_enrolled: int = courses_enrolled

    def get_stipend_rate(self) -> float:
        return self.__stipend_rate

    def get_courses_enrolled(self) -> int:
        return self.__courses_enrolled

    def calculate_monthly_payout(self) -> float:
        """
        Returns stipend minus 2% welfare deduction.
        e.g. ₦50,000 stipend → ₦49,000 payout (₦1,000 deducted)
        """
        deduction = self.__stipend_rate * self.WELFARE_DEDUCTION_RATE
        return self.__stipend_rate - deduction

    def __str__(self) -> str:
        base = super().__str__()
        return (
            f"{base}\n"
            f"  Stipend: ₦{self.__stipend_rate:,.2f} | "
            f"Courses: {self.__courses_enrolled} | "
            f"Monthly Payout: ₦{self.calculate_monthly_payout():,.2f}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# DERIVED CLASS 2: LecturerUser  (inherits from User)
# ══════════════════════════════════════════════════════════════════════════════

class LecturerUser(User):
    """
    Represents a lecturer/staff member in the institutional system.

    Monthly payout = base_salary + (overtime_hours × hourly_rate)
    """

    def __init__(self, user_id: str, full_name: str, email: str,
                 base_salary: float, overtime_hours: int, hourly_rate: float):
        """
        Args:
            base_salary (float): Fixed monthly salary (must be > 0).
            overtime_hours (int): Extra hours worked this month (>= 0).
            hourly_rate (float): Pay per overtime hour (must be > 0).
        """
        super().__init__(user_id, full_name, email)

        if base_salary <= 0:
            raise ValueError("Base salary must be greater than zero.")
        if overtime_hours < 0:
            raise ValueError("Overtime hours cannot be negative.")
        if hourly_rate <= 0:
            raise ValueError("Hourly rate must be greater than zero.")

        self.__base_salary: float = base_salary
        self.__overtime_hours: int = overtime_hours
        self.__hourly_rate: float = hourly_rate

    def get_base_salary(self) -> float:
        return self.__base_salary

    def get_overtime_hours(self) -> int:
        return self.__overtime_hours

    def get_hourly_rate(self) -> float:
        return self.__hourly_rate

    def calculate_monthly_payout(self) -> float:
        """
        Returns base salary plus overtime pay.
        e.g. ₦300,000 base + (10 hours × ₦5,000) = ₦350,000
        """
        overtime_pay = self.__overtime_hours * self.__hourly_rate
        return self.__base_salary + overtime_pay

    def __str__(self) -> str:
        base = super().__str__()
        return (
            f"{base}\n"
            f"  Base Salary: ₦{self.__base_salary:,.2f} | "
            f"Overtime: {self.__overtime_hours}hrs @ ₦{self.__hourly_rate:,.2f}/hr | "
            f"Monthly Payout: ₦{self.calculate_monthly_payout():,.2f}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# DERIVED CLASS 3: ResearchAssistant  (inherits from StudentUser)
# — demonstrates MULTI-LEVEL inheritance: User → StudentUser → ResearchAssistant
# ══════════════════════════════════════════════════════════════════════════════

class ResearchAssistant(StudentUser):
    """
    Represents a student who also works as a research assistant.

    Inherits from StudentUser (which already inherits from User),
    creating a 3-level inheritance chain:
        User → StudentUser → ResearchAssistant

    Monthly payout = StudentUser's payout + research grant allowance.
    """

    def __init__(self, user_id: str, full_name: str, email: str,
                 stipend_rate: float, courses_enrolled: int,
                 research_grant_allowance: float):
        """
        Args:
            research_grant_allowance (float): Additional monthly research grant (>= 0).
        """
        super().__init__(user_id, full_name, email, stipend_rate, courses_enrolled)

        if research_grant_allowance < 0:
            raise ValueError("Research grant allowance cannot be negative.")

        self.__research_grant_allowance: float = research_grant_allowance

    def get_research_grant_allowance(self) -> float:
        return self.__research_grant_allowance

    def calculate_monthly_payout(self) -> float:
        """
        Calls StudentUser's payout calculation and adds the research grant.
        This is the correct way to extend a parent's method using super().
        """
        student_payout = super().calculate_monthly_payout()
        return student_payout + self.__research_grant_allowance

    def __str__(self) -> str:
        base = super().__str__()
        return (
            f"{base} + Grant: ₦{self.__research_grant_allowance:,.2f} | "
            f"Total Payout: ₦{self.calculate_monthly_payout():,.2f}"
        )
