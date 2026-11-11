import { Suspense } from "react";
import { ResetPasswordForm } from "./ResetPasswordForm";

export const metadata = { title: "Set password" };

export default function ResetPasswordPage() {
  return (
    <Suspense>
      <ResetPasswordForm />
    </Suspense>
  );
}
