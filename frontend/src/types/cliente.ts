export interface ClienteBase {
  nombre: string;
  documento: string;
  contacto: string;
}

export interface ClienteCreate extends ClienteBase {}

export interface ClienteRead extends ClienteBase {
  id: number;
}

export type Cliente = ClienteRead;
