import React, { useCallback, useEffect, useState } from 'react';

interface ComponentProps {
  userId: string;
}

export default function Settings(props: ComponentProps) {
  const { userId } = props;
  const [isPublic, setIsPublic] = useState(true);

  useEffect(() => {
    fetch('/api/user')
      .then((res) => res.json())
      .then((data) => {
        setIsPublic(!data.is_private);
      })
      .catch(() => {});
  }, [userId]);

  const onChange = useCallback((event: any) => {
    fetch('/api/settings', {
      method: 'POST',
      body: JSON.stringify({
        is_public: event.target.checked,
      }),
    })
      .then((res) => res.json())
      .then(() => {
      })
      .catch(() => {});
    setIsPublic(event.target.checked);
  }, []);

  return (
    <div>
      Public Profile
      <input
        id="is-public-checkbox"
        type="checkbox"
        name="isPublic"
        checked={isPublic}
        onChange={onChange}
      />
    </div>
  );
}
