"""
CSL 112: Introduction to Advanced Level Programming
Independent Lab Activity: Encapsulation & Secure Class Design

academic_portal.py (Version 3)

Design differences from Versions 1 & 2:
  - Built on @dataclass, with __post_init__ doing constructor validation
    (instead of a hand-written __init__).
  - A reusable `@validated_setter` decorator wraps mutator methods so the
    "reject bad input, raise, keep old value" pattern isn't copy-pasted
    per method.
  - True privacy is still enforced the same way Python always enforces
    it: double-underscore attributes, name-mangled by the interpreter.
"""

from dataclasses import dataclass, field
from functools import wraps


def validated_setter(validator):
    """
    Decorator factory for mutator methods.

    `validator` is a function (self, value) -> None that raises
    ValueError if `value` is unacceptable. The decorated method only
    runs its body if validation passes.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, value, *args, **kwargs):
            validator(self, value)
            return func(self, value, *args, **kwargs)
        return wrapper
    return decorator


def _check_cgpa(self, value):
    if not isinstance(value, (int, float)):
        raise ValueError("CGPA must be numeric.")
    if not (Student.MIN_CGPA <= value <= Student.MAX_CGPA):
        raise ValueError(
            f"CGPA {value} is out of bounds "
            f"[{Student.MIN_CGPA:.2f}, {Student.MAX_CGPA:.2f}]."
        )


def _check_payment(self, value):
    if not isinstance(value, (int, float)):
        raise ValueError("Payment amount must be numeric.")
    if value <= 0:
        raise ValueError(f"Payment amount must be > 0 (got {value}).")


@dataclass
class Student:
    """
    Represents a student's academic record.

    NOTE: dataclass fields are declared with a single leading underscore
    (a *convention* for "internal use") but the real enforcement of
    privacy comes from wrapping them behind double-underscore aliases
    set up in __post_init__ -- dataclasses don't support name-mangled
    (__x) fields directly, since Python would mangle the field name
    itself at class-definition time in a way that breaks dataclass
    introspection. So __post_init__ transfers validated values into
    genuinely mangled private storage.
    """

    MIN_CGPA = 0.00
    MAX_CGPA = 5.00

    matric_no: str
    name: str
    initial_balance: float

    def __post_init__(self):
        if not isinstance(self.matric_no, str) or not self.matric_no.strip():
            raise ValueError("matric_no must be a non-empty string.")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string.")
        if not isinstance(self.initial_balance, (int, float)):
            raise ValueError("initial_balance must be numeric.")
        if self.initial_balance < 0:
            raise ValueError(
                f"initial_balance cannot be negative (got {self.initial_balance})."
            )

        # Move into genuinely private, name-mangled storage and drop the
        # public dataclass-generated fields so external code can't just
        # read/write self.initial_balance directly.
        self.__matric_number = self.matric_no
        self.__full_name = self.name
        self.__cgpa = self.MIN_CGPA
        self.__tuition_balance = float(self.initial_balance)

        # Remove the raw public fields dataclass created on the instance.
        del self.matric_no, self.name, self.initial_balance

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------
    def get_matric_number(self) -> str:
        return self.__matric_number

    def get_full_name(self) -> str:
        return self.__full_name

    def get_cgpa(self) -> float:
        return self.__cgpa

    def get_tuition_balance(self) -> float:
        return self.__tuition_balance

    # ------------------------------------------------------------------
    # Validated mutators
    # ------------------------------------------------------------------
    @validated_setter(_check_cgpa)
    def update_cgpa(self, new_cgpa: float) -> None:
        self.__cgpa = float(new_cgpa)

    @validated_setter(_check_payment)
    def pay_tuition(self, amount: float) -> None:
        self.__tuition_balance -= amount

    # ------------------------------------------------------------------
    # Lifecycle management
    # ------------------------------------------------------------------
    def __del__(self):
        matric = getattr(self, "_Student__matric_number", "UNKNOWN")
        print(f"[SESSION CLOSED] Student record for {matric} safely deallocated.")

    def __repr__(self):
        return (
            f"<Student {self.__matric_number} | {self.__full_name} | "
            f"CGPA={self.__cgpa:.2f} | Balance={self.__tuition_balance:.2f}>"
        )


class Department:
    """An academic department that manages a private roster of Students."""

    def __init__(self, dept_name: str):
        if not isinstance(dept_name, str) or not dept_name.strip():
            raise ValueError("dept_name must be a non-empty string.")
        self.dept_name = dept_name
        self.__students_list = []

    def add_student(self, student_object: Student) -> None:
        if not isinstance(student_object, Student):
            raise TypeError(
                f"Expected a Student instance, got {type(student_object).__name__}."
            )
        self.__students_list.append(student_object)

    def get_students(self) -> list:
        return list(self.__students_list)

    def generate_honors_roll(self, threshold: float = 3.50) -> list:
        print(f"\n--- {self.dept_name} Department: Honors Roll (CGPA >= {threshold:.2f}) ---")
        honors = [s for s in self.__students_list if s.get_cgpa() >= threshold]

        if honors:
            for s in honors:
                print(f"  {s.get_full_name()} ({s.get_matric_number()}): {s.get_cgpa():.2f}")
        else:
            print("  No students currently qualify for the honors roll.")

        print("-------------------------------------------------------------\n")
        return honors
