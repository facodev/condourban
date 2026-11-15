import { Component, ViewEncapsulation, input, output, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatRipple } from '@angular/material/core';

export interface TableColumn<T = any> {
  key: string;
  header: string;
  sortable?: boolean;
  width?: string;
  formatter?: (row: T) => string;
}

@Component({
  selector: 'app-data-table',
  standalone: true,
  imports: [CommonModule, FormsModule, MatRipple],
  templateUrl: './data-table.component.html',
  styleUrls: ['./data-table.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class DataTableComponent<T = any> {
  readonly columns = input<TableColumn<T>[]>([]);
  readonly data = input<T[]>([]);
  readonly pageSize = input<number>(10);

  readonly rowClick = output<T>();

  readonly sortKey = signal<string | null>(null);
  readonly sortAsc = signal<boolean>(true);
  readonly currentPage = signal<number>(1);
  readonly customPageSize = signal<number | null>(null);

  readonly effectivePageSize = computed(() => this.customPageSize() ?? this.pageSize());

  readonly hasRowClick = computed(() => this.rowClick !== undefined);

  readonly sortedData = computed(() => {
    const list = [...this.data()];
    const key = this.sortKey();
    if (!key) return list;

    const asc = this.sortAsc();
    return list.sort((a: any, b: any) => {
      const valA = a[key];
      const valB = b[key];
      if (valA < valB) return asc ? -1 : 1;
      if (valA > valB) return asc ? 1 : -1;
      return 0;
    });
  });

  readonly totalPages = computed(() => {
    return Math.max(1, Math.ceil(this.sortedData().length / this.effectivePageSize()));
  });

  readonly paginatedData = computed(() => {
    const size = this.effectivePageSize();
    const page = Math.min(this.currentPage(), this.totalPages());
    const start = (page - 1) * size;
    return this.sortedData().slice(start, start + size);
  });

  readonly startIndex = computed(() => {
    if (this.sortedData().length === 0) return 0;
    return (Math.min(this.currentPage(), this.totalPages()) - 1) * this.effectivePageSize() + 1;
  });

  readonly endIndex = computed(() => {
    return Math.min(this.sortedData().length, this.startIndex() + this.paginatedData().length - 1);
  });

  readonly pagesArray = computed(() => {
    const total = this.totalPages();
    return Array.from({ length: total }, (_, i) => i + 1);
  });

  toggleSort(key: string): void {
    if (this.sortKey() === key) {
      this.sortAsc.update(v => !v);
    } else {
      this.sortKey.set(key);
      this.sortAsc.set(true);
    }
    this.currentPage.set(1);
  }

  changePage(page: number): void {
    if (page >= 1 && page <= this.totalPages()) {
      this.currentPage.set(page);
    }
  }

  onPageSizeChange(newSize: number): void {
    this.customPageSize.set(Number(newSize));
    this.currentPage.set(1);
  }

  getCellValue(row: T, key: string): any {
    return (row as Record<string, any>)?.[key];
  }
}
