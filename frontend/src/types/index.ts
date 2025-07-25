// src/types/index.ts

/**
 * Este arquivo centraliza todas as tipagens de dados compartilhadas
 * entre o frontend e a API do backend, garantindo consistência.
 */

// =================================
// Tipos de Autenticação e Usuário
// =================================

export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

// =================================
// Tipos de Transações
// =================================

export interface Transaction {
  id: number;
  owner_id: number;
  description: string;
  amount: number;
  date: string; // As datas são serializadas como strings no formato ISO (ex: "2024-07-25T12:00:00")
  category_id: number;
}

export interface TransactionCreate {
  description: string;
  amount: number;
  date: string;
  category_id: number;
}

// =================================
// Tipos de Categorias
// =================================

export type CategoryType = 'income' | 'expense';

export interface Category {
  id: number;
  owner_id: number;
  name: string;
  type: CategoryType;
}

export interface CategoryCreate {
  name: string;
  type: CategoryType;
}

// =================================
// Tipos de Metas (Goals)
// =================================

export interface Goal {
  id: number;
  owner_id: number;
  name: string;
  target_amount: number;
  current_amount: number;
  due_date?: string; // Data no formato "YYYY-MM-DD"
}

export interface GoalCreate {
  name: string;
  target_amount: number;
  current_amount?: number;
  due_date?: string;
}

// =================================
// Tipos de Sessões de Trabalho
// =================================

export interface WorkSession {
  id: number;
  owner_id: number;
  start_time: string; // Data e hora no formato ISO
  end_time?: string;
  platform: string;
  earnings?: number;
}

export interface WorkSessionCreate {
  start_time: string;
  end_time?: string;
  platform: string;
  earnings?: number;
}


// =================================
// Tipos para Endpoints Específicos
// =================================

export interface DateRange {
  start_date: string; // Data no formato "YYYY-MM-DD"
  end_date: string;
}

export interface MonthlyPerformance {
  month: string;
  income: number;
  expense: number;
  net: number;
}

export interface PlatformBreakdown {
    earnings: number;
    hours: number;
    hourly_rate: number;
}

export interface ComprehensiveProfile {
  user_info: User;
  total_income: number;
  total_expense: number;
  net_income: number;
  total_hours_worked: number;
  average_hourly_rate: number;
  monthly_performance: MonthlyPerformance[];
  category_breakdown: Record<string, number>; // Ex: { "Alimentação": 500.50, "Combustível": 800.00 }
  platform_breakdown: Record<string, PlatformBreakdown>; // Ex: { "Uber": { earnings: 1200, ... } }
  recent_transactions: Transaction[];
  active_goals: Goal[];
}
