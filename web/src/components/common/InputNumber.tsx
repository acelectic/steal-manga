import { Input, InputProps } from 'antd'
import { ForwardRefRenderFunction, forwardRef } from 'react'
import { NumericFormat, NumericFormatProps } from 'react-number-format'

interface IInputNumberProps
  extends Omit<
    NumericFormatProps<InputProps>,
    'value' | 'onChange' | 'onValueChange' | 'customInput' | 'defaultValue'
  > {
  value?: number
  onChange?: (value?: number) => void
}

const InputNumberBase: ForwardRefRenderFunction<HTMLInputElement, IInputNumberProps> = (
  props,
  ref,
) => {
  const { value, onChange, ...restProps } = props
  return (
    <NumericFormat
      getInputRef={ref}
      value={value}
      onValueChange={(d) => {
        onChange?.(d.floatValue)
      }}
      customInput={Input}
      {...restProps}
    />
  )
}

export const InputNumber = forwardRef(InputNumberBase)
