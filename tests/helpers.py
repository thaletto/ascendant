from typing import Any, List, Tuple


def print_timing_summary(
    title: str,
    total_elapsed: float,
    timings: List[Tuple[Any, float]],
    unit_name: str,
    top_n: int = 10,
):
    """Prints a standardized timing summary."""
    if not timings:
        return

    print(f"\n{'=' * 70}")
    print(f"{title.upper()} TIMING SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total time: {total_elapsed:.4f} seconds")
    print(f"Number of {unit_name}s: {len(timings)}\n")

    # Sort by time (slowest first)
    timings.sort(key=lambda x: x[1], reverse=True)
    print(f"Top {top_n} slowest {unit_name}s:")
    print("-" * 70)

    for item, elapsed in timings[:top_n]:
        percentage = (elapsed / total_elapsed) * 100 if total_elapsed > 0 else 0
        if isinstance(item, str):
            # For string items like yoga names, left-align them
            print(f"  {item:<30s}: {elapsed:8.6f} seconds ({percentage:5.2f}%)")
        else:
            # For other items like division numbers
            print(
                f"  {unit_name.capitalize()} {str(item):<10s}: {elapsed:8.6f} seconds ({percentage:5.2f}%)"
            )

    if len(timings) > top_n:
        print(f"\n... and {len(timings) - top_n} more {unit_name}s\n")
    else:
        print()

    # Print statistics
    times = [t[1] for t in timings]
    avg_time = sum(times) / len(times) if times else 0
    min_time = min(times) if times else 0
    max_time = max(times) if times else 0

    print("Statistics:")
    print(f"\nAverage time per {unit_name}: {avg_time:.6f} seconds")
    print(f"Fastest {unit_name}: {min_time:.6f} seconds")
    print(f"Slowest {unit_name}: {max_time:.6f} seconds")
    print(f"{'=' * 70}\n")


def format_and_print_table(headers: List[str], rows: List[List[str]], title: str = ""):
    """Formats and prints a table using prettytable if available, else manual."""
    try:
        from prettytable import PrettyTable

        table = PrettyTable()
        if title:
            table.title = title
        table.field_names = headers
        table.align = "l"
        for row in rows:
            table.add_row(row)

        print(str(table))

    except ImportError:
        print(f"\n--- {title} ---" if title else "\n--- TABLE ---")

        all_lines = [headers] + [[str(c) for c in r] for r in rows]

        col_widths = [max(len(item) for item in col) for col in zip(*all_lines)]

        def format_row(vals):
            return " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(vals))

        print(format_row(headers))
        print("-+-".join("-" * w for w in col_widths))
        for r in rows:
            print(format_row(r))
        print("--- END ---\\n")
